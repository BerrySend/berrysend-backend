from pydantic import BaseModel, Field

class UpdatePortRequest(BaseModel):
    """
    Request schema for updating a port.

    Attributes:
        name (str): The name of the port.
        port_type (str): The type of the port (e.g., "initial", "intermediate", "destination").
    """
    name: str = Field(title="The name of the port")
    port_type: str = Field(title="The type of the port")

    # Defines a JSON schema extra field to include examples in the OpenAPI schema.
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Shanghai",
                    "port_type": "destination",
                }
            ]
        }
    }