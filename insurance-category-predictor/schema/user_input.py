from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Literal, Annotated
from ..config import tier_1_cities, tier_2_cities

#pydantic model to validate incoming data from client
class Input(BaseModel):
    age: Annotated[int, Field(..., gt=16, lt=100, description="age of user")]
    weight: Annotated[float, Field(..., gt=30, lt=300, description="enter the weight")]
    height: Annotated[float, Field(..., gt=0, lt=3, description="give height in meters")]
    income_lpa: Annotated[float, Field(..., description="Income of user in lacks per annum")]
    smoker: Annotated[bool, Field(..., description="true or false")]
    city: Annotated[str, Field(..., description="city in which the user lives")]
    occupation: Annotated[Literal['student', 'retired', 'freelancer', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description="occupation of the user")]

    # field validator to convert city name to title case - maintaining case consistency
    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title()
        return v

    # Following are the features derived from the input featues. 
    # The model accepts only these and hence we will need to calculate them.

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi >30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        if self.age < 45:
            return "adult"
        if self.age < 65:
            return "middle_aged"
        else:
            return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3