from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.supabase import supabase

router = APIRouter()

class PQRSRequest(BaseModel):
    titulo: str
    tipo: str
    descripcion: str
    usuario_id: str

class PQRSUpdateRequest(PQRSRequest):  # 🔁 NUEVO MODELO CON ESTADO
    estado: str

@router.post("/")
def crear_pqrs(pqrs: PQRSRequest):
    try:
        data = pqrs.dict()
        data["estado"] = "pendiente"
        result = supabase.table("pqrs").insert(data).execute()
        return {"mensaje": "PQRS creada", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def obtener_todas_las_pqrs():
    try:
        result = supabase.table("pqrs").select("*").execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{usuario_id}")
def obtener_pqrs_por_usuario(usuario_id: str):
    try:
        result = supabase.table("pqrs").select("*").eq("usuario_id", usuario_id).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/id/{pqrs_id}")
def obtener_pqrs_por_id(pqrs_id: str):
    try:
        result = supabase.table("pqrs").select("*").eq("id", pqrs_id).single().execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{pqrs_id}")  # 🔁 AQUÍ EL CAMBIO
def actualizar_pqrs(pqrs_id: str, pqrs: PQRSUpdateRequest):
    try:
        result = supabase.table("pqrs").update(pqrs.dict()).eq("id", pqrs_id).execute()
        return {"mensaje": "PQRS actualizada", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{pqrs_id}")
def eliminar_pqrs(pqrs_id: str):
    try:
        result = supabase.table("pqrs").delete().eq("id", pqrs_id).execute()
        return {"mensaje": "PQRS eliminada", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
