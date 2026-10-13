from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field

class CategoriaBokatas(str, Enum):
    PANADERIA = "Panadería"
    EMBUTIDOS = "Embutidos"
    QUESOS = "Quesos"
    BEBIDAS = "Bebidas"
    TORTILLAS = "Tortillas"
    FRUTAS_VERDURAS = "Frutas y Verduras"
    DESECHABLES_ENSERES = "Desechables y Enseres"
    LOGISTICA_TRANSPORTE = "Logística y Transporte"
    OTROS = "Otros"

class LineaGastoCategoria(BaseModel):
    categoria: CategoriaBokatas = Field(
        ..., 
        description="Standardized budgetary accounting category for Asociación Bokatas"
    )
    concepto: str = Field(..., description="Product description (e.g. Barra de pan, Jamón York, Servilletas)")
    cantidad: Optional[float] = Field(None, description="Purchased quantity")
    precio_unitario: Optional[float] = Field(None, description="Unit price in EUR")
    importe_linea: float = Field(..., description="Total line amount in EUR")

class DatosFacturaBokatas(BaseModel):
    fecha_factura: str = Field(..., description="Invoice date in YYYY-MM-DD format")
    sede: str = Field(..., description="Operating chapter/branch (e.g. Madrid-Centro, Valencia, Zaragoza)")
    proveedor: str = Field(..., description="Normalized vendor name (e.g. Mercadona, Carrefour, Local Bakery)")
    cif_nif_proveedor: Optional[str] = Field(None, description="Tax ID / CIF / NIF of supplier if available")
    numero_factura: str = Field(
        ..., 
        description="Invoice or receipt sequential number (e.g. '0147', 'FAC-2023-99', 'T-88472')"
    )
    importe_total: float = Field(..., description="Total invoice amount charged in EUR")
    metodo_pago: Optional[str] = Field(None, description="Payment method (Card, Cash, Bank Transfer)")
    desglose_categorias: List[LineaGastoCategoria] = Field(
        default_factory=list, 
        description="Itemized lines mapped into official accounting categories"
    )
    observaciones: Optional[str] = Field(None, description="Operational remarks or OCR quality warnings")
