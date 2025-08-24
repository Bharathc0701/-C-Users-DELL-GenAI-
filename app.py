import os
import uuid
import tempfile
import subprocess
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from supabase import create_client, Client
from docxtpl import DocxTemplate

# -------- Env & Supabase --------
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # service role key
BUCKET = os.getenv("SUPABASE_BUCKET", "agreements")
TEMPLATE_PATH = os.getenv("DOCX_TEMPLATE", "templates/rental_template.docx")
PDF_ENGINE = os.getenv("PDF_ENGINE", "docx2pdf")  # docx2pdf | libreoffice
PRIVATE_BUCKET = os.getenv("PRIVATE_BUCKET", "true").lower() == "true"

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY in .env")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Rental Agreement Generator")

# Allow your Lovable app to call this API in dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Models --------
class GeneratePayload(BaseModel):
    record_id: str                 # UUID of rental_agreements.id
    overrides: Optional[Dict[str, Any]] = None
    visibility: Optional[str] = None  # "public" or "private"

# -------- Helpers --------
def fetch_agreement(record_id: str) -> Dict[str, Any]:
    res = supabase.table("rental_agreements").select("*").eq("id", record_id).single().execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Agreement not found")
    return res.data

def build_context(data: Dict[str, Any], overrides: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    ctx = {
        # Property
        "agreement_execution_date": str(data.get("agreement_execution_date") or ""),
        "project_name": data.get("project_name"),
        "unit_number": data.get("unit_number"),
        "project_address": data.get("project_address"),
        "rent": data.get("rent"),
        "maintenance": data.get("maintenance"),
        "security_deposit": data.get("security_deposit"),
        "sd_payment_date": str(data.get("sd_payment_date") or ""),
        "sd_payment_mode": data.get("sd_payment_mode"),
        "move_in_date": str(data.get("move_in_date") or ""),

        # Owner
        "owner_salutation": data.get("owner_salutation"),
        "owner_name": data.get("owner_name"),
        "owner_relation_type": data.get("owner_relation_type"),
        "owner_guardian": data.get("owner_guardian"),
        "owner_age": data.get("owner_age"),
        "owner_address": data.get("owner_address"),
        "owner_aadhar": data.get("owner_aadhar"),
        "owner_mobile": data.get("owner_mobile"),
        "owner_email": data.get("owner_email"),
        "ownership_proof": data.get("ownership_proof"),

        # Tenants (array of dicts)
        "tenants": data.get("tenants") or [],

        # In-words
        "rent_in_words": data.get("rent_in_words"),
        "maintenance_in_words": data.get("maintenance_in_words"),
        "security_deposit_in_words": data.get("security_deposit_in_words"),

        # Bank
        "owner_bank_account_name": data.get("owner_bank_account_name"),
        "owner_bank_account_number": data.get("owner_bank_account_number"),
        "owner_bank_name": data.get("owner_bank_name"),
        "owner_bank_branch": data.get("owner_bank_branch"),
        "owner_bank_ifsc_code": data.get("owner_bank_ifsc_code"),
        "owner_bank_upi_id": data.get("owner_bank_upi_id"),
    }
    if overrides:
        ctx.update(overrides)
    # convert None -> "" for safety in template
    def _clean(v):
        if isinstance(v, list):
            return [ {k: ("" if vv is None else vv) for k, vv in d.items()} if isinstance(d, dict) else d for d in v ]
        if isinstance(v, dict):
            return {k: ("" if vv is None else vv) for k, vv in v.items()}
        return "" if v is None else v
    return {k: _clean(v) for k, v in ctx.items()}

def render_docx(context: Dict[str, Any]) -> str:
    if not os.path.exists(TEMPLATE_PATH):
        raise HTTPException(status_code=500, detail="Template not found on server")
    doc = DocxTemplate(TEMPLATE_PATH)
    doc.render(context)
    tmp_docx = os.path.join(tempfile.gettempdir(), f"agreement-{uuid.uuid4()}.docx")
    doc.save(tmp_docx)
    return tmp_docx

def convert_to_pdf(docx_path: str) -> str:
    pdf_path = docx_path.replace(".docx", ".pdf")
    engine = (PDF_ENGINE or "docx2pdf").lower()

    if engine == "docx2pdf":
        from docx2pdf import convert as docx2pdf_convert
        docx2pdf_convert(docx_path, pdf_path)
        return pdf_path

    if engine == "libreoffice":
        out_dir = os.path.dirname(docx_path)
        cmd = ["soffice", "--headless", "--convert-to", "pdf", "--outdir", out_dir, docx_path]
        subprocess.run(cmd, check=True)
        return pdf_path

    raise HTTPException(status_code=500, detail="Unsupported PDF engine")

def upload_pdf_to_supabase(record_id: str, pdf_path: str, visibility: Optional[str]) -> tuple[str, str]:
    key = f"rental-agreements/{record_id}/{uuid.uuid4()}.pdf"
    with open(pdf_path, "rb") as f:
        supabase.storage.from_(BUCKET).upload(key, f, file_options={"content-type": "application/pdf"})

    want_public = (visibility == "public")

    if want_public or (not PRIVATE_BUCKET and visibility != "private"):
        url = supabase.storage.from_(BUCKET).get_public_url(key)
        return key, url

    signed = supabase.storage.from_(BUCKET).create_signed_url(key, expires_in=60 * 60 * 24 * 7)
    return key, signed.get("signedURL")

def update_agreement_with_pdf(record_id: str, file_url: str):
    supabase.table("rental_agreements").update({
        "pdf_url": file_url,
        "pdf_generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "Generated",
        "is_draft": False
    }).eq("id", record_id).execute()

# -------- Routes --------
@app.get("/ping")
def ping():
    return {"ok": True}

@app.post("/generate-agreement")
def generate_agreement(payload: GeneratePayload):
    # 1) Fetch row
    data = fetch_agreement(payload.record_id)

    # 2) Build template context
    context = build_context(data, payload.overrides)

    # 3) Render DOCX
    docx_path = render_docx(context)

    # 4) Convert to PDF
    pdf_path = convert_to_pdf(docx_path)

    # 5) Upload to Supabase Storage
    _, url = upload_pdf_to_supabase(payload.record_id, pdf_path, payload.visibility)

    # 6) Update agreement row
    update_agreement_with_pdf(payload.record_id, url)

    return {"status": "success", "record_id": payload.record_id, "pdf_url": url}
