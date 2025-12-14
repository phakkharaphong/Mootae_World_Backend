from pydantic import BaseModel, ConfigDict, Field


class AttachmentGetDto(BaseModel):
    id: str | None = Field(
        description="ID Attachment",
        default="EXasfew565d2"
    )
    
    fileName: str | None = Field(
        description="File Name",
        default="download.pdf"
    )
    
    content_type: str | None = Field(
        description="Content Type",
        default="application/pdf"
    )
    
    fileLocation: str | None = Field(
        description="Path File for Upload",
        default="UploadedFiles/download.pdf"
    )
    
    fileSize: int | None = Field(
        description="Size File Upload",
        default=100
    )
    
    mime: str | None = Field(
        description="Mime File",
        default=".pdf"
    )

    model_config = ConfigDict(from_attributes=True)


class AttachmentCreateDto(BaseModel):
    fileName: str | None = Field(
        description="File Name",
        default="download.pdf"
    )
    
    content_type: str | None = Field(
        description="Content Type",
        default="application/pdf"
    )
    
    fileLocation: str | None = Field(
        description="Path File for Upload",
        default="UploadedFiles/download.pdf"
    )
    
    fileSize: int | None = Field(
        description="Size File Upload",
        default=100
    )
    
    mime: str | None = Field(
        description="Mime File",
        default=".pdf"
    )

    model_config = ConfigDict(from_attributes=True)
