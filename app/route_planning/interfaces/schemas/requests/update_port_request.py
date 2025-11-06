from pydantic import BaseModel

class UpdatePortRequest(BaseModel):
    """
    Request schema for updating a port.

    Attributes:
        name (str): The name of the port.
        port_type (str): The type of the port (e.g., "initial", "intermediate", "destination").", "
    """
    name: str
    port_type: str