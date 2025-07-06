from typing import List
from pydantic import BaseModel, Field

# main_dto.py

from pydantic import BaseModel, Field
from typing import List

# --- 巢狀基礎模型 (由內而外定義) ---

class ValueJustification(BaseModel):
    """用於表示一個值、其可信度分數和理由的通用結構。"""
    value: str = Field(..., description="提取或推斷出的主要值。")
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="模型對該值準確性的可信度分數，範圍在 0.0 到 1.0 之間。"
    )
    justification: str = Field(..., description="提供此值的簡要理由或證據來源。")

class FeatureJustification(BaseModel):
    """用於描述軟體功能及其相關分析的結構。"""
    feature: str = Field(..., description="描述一個具體的軟體功能。")
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="模型對該功能存在的可信度分數，範圍在 0.0 到 1.0 之間。"
    )
    justification: str = Field(..., description="解釋為什麼認為此功能存在或很重要。")

class Persona(BaseModel):
    """描述一個具體的目標用戶畫像。"""
    name: str = Field(..., description="用戶畫像的名稱，例如 '忙碌的上班族' 或 '技術愛好者'。")
    type: str = Field(..., description="用戶畫像的分類，例如 'End User', 'Administrator', 'Developer'。")
    userStory: str = Field(..., description="描述該用戶需求的用戶故事，格式為：'身為一個 <角色>, 我想要 <目標>, 如此一來 <價值>。'")
    goals: List[str] = Field(..., description="該用戶畫像使用此應用的主要目標列表。")
    painPoints: List[str] = Field(..., description="該用戶畫像在沒有此應用時可能遇到的痛點或挑戰列表。")
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="模型對此用戶畫像分析準確性的可信度分數。"
    )
    behavioralEvidence: str = Field(..., description="從輸入文本中找到的，支持此用戶畫像存在的行為證據。")

class TargetAudiencePersonas(BaseModel):
    """包含主要、次要和邊緣案例用戶畫像的集合。"""
    primary: List[Persona] = Field(..., description="主要目標用戶畫像列表。")
    secondary: List[Persona] = Field(..., description="次要目標用戶畫像列表。")
    edgeCases: List[Persona] = Field(..., description="需要考慮的邊緣案例或非典型用戶畫像列表。")

class TechnologyStackItem(BaseModel):
    """描述技術棧中的一個具體項目。"""
    category: str = Field(..., description="技術的分類，例如 'Frontend Framework', 'Database', 'Cloud Provider', 'Backend Language'。")
    name: str = Field(..., description="技術的具體名稱，例如 'React', 'PostgreSQL', 'AWS', 'Python'。")
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="模型對該技術被使用的可信度分數。"
    )
    inferredVia: str = Field(..., description="推斷出此技術的邏輯或原因。")
    detectedFrom: str = Field(..., description="從輸入文本中檢測到此技術的具體詞語或句子。")

class QualityAttribute(BaseModel):
    """描述一個推斷出的非功能性需求或品質屬性。"""
    attribute: str = Field(..., description="品質屬性的名稱，例如 'Scalability', 'Security', 'Usability', 'Performance'。")
    confidenceScore: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="模型對此品質屬性重要性的可信度分數。"
    )
    justification: str = Field(..., description="解釋為什麼認為此品質屬性對該應用很重要。")


# --- 最上層的主模型 ---

class WebExtractedInfo(BaseModel):
    """
    用於對軟體應用描述進行全面分析的結構化輸出。
    請根據提供的文本，完整填寫所有欄位。
    """
    applicationType: ValueJustification = Field(..., description="應用的類型分析，例如 'SaaS', 'Mobile App', 'Internal Tool'。")
    coreBusinessGoal: ValueJustification = Field(..., description="應用的核心商業目標或要解決的主要問題。")
    supportingFunctionality: List[FeatureJustification] = Field(..., description="支撐核心目標所需的主要功能列表。")
    targetAudiencePersonas: TargetAudiencePersonas = Field(..., description="對目標用戶的詳細畫像分析。")
    technologyStack: List[TechnologyStackItem] = Field(..., description="從文本中推斷或檢測到的技術棧。")
    inferredQualityAttributes: List[QualityAttribute] = Field(..., description="推斷出的重要非功能性需求（品質屬性）。")
