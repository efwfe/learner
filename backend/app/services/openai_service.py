"""
Azure OpenAI 服务 - 用于知识点生成、总结和知识体系构建
"""
from typing import List, Dict, Optional
import json
from openai import AzureOpenAI
from ..core.config import settings
from logging import getLogger


logger = getLogger(__name__)

class OpenAIService:
    """Azure OpenAI 服务封装"""
    
    def __init__(self):
        self.client = None
        if settings.AZURE_OPENAI_API_KEY and settings.AZURE_OPENAI_ENDPOINT:
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.AZURE_OPENAI_API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
    
    def is_available(self) -> bool:
        """检查 OpenAI 服务是否可用"""
        return self.client is not None
    
    async def generate_knowledge_summary(self, title: str, content: str) -> str:
        """
        生成知识点摘要
        
        Args:
            title: 知识点标题
            content: 知识点内容
            
        Returns:
            生成的摘要
        """
        if not self.is_available():
            return "OpenAI 服务未配置"
        
        prompt = f"""请为以下知识点生成一个简洁的摘要（100字以内）：

标题：{title}

内容：
{content}

摘要应该：
1. 提炼核心概念
2. 突出关键要点
3. 便于快速回顾
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的学习助手，擅长提炼知识要点。"},
                    {"role": "user", "content": prompt}
                ],
                #temperature=0.7,
                max_completion_tokens=300
            )
            
            result =  response.choices[0].message.content.strip()
            logger.info(f"generate_knowledge_summary result: {result}")
            return result
        except Exception as e:
            return f"生成摘要失败: {str(e)}"
    
    async def extract_knowledge_points(self, learning_content: str) -> List[Dict[str, str]]:
        """
        从学习内容中提取知识点
        
        Args:
            learning_content: 学习内容
            
        Returns:
            提取的知识点列表 [{"title": "...", "content": "...", "category": "..."}]
        """
        if not self.is_available():
            return []
        
        prompt = f"""请从以下学习内容中提取关键知识点，以JSON格式返回：

{learning_content}

要求：
1. 识别所有重要的概念、定义、方法等
2. 每个知识点包含：title（标题）、content（详细内容）、category（分类）
3. 返回JSON数组格式

示例格式：
[
  {{"title": "知识点标题", "content": "详细说明", "category": "分类"}},
  ...
]
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的知识提取助手。请严格按照JSON格式返回结果。"},
                    {"role": "user", "content": prompt}
                ],
                # #temperature=0.5,
                max_completion_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            
            # 尝试解析JSON
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            knowledge_points = json.loads(content.strip())
            logger.info(f"extract_knowledge_points knowledge_points: {knowledge_points}")
            return knowledge_points
        except Exception as e:
            print(f"提取知识点失败: {str(e)}")
            return []
    
    async def suggest_knowledge_relations(
        self,
        knowledge_point: Dict[str, str],
        existing_points: List[Dict[str, str]]
    ) -> List[Dict[str, any]]:
        """
        建议知识点之间的关系
        
        Args:
            knowledge_point: 当前知识点 {"id": 1, "title": "...", "content": "..."}
            existing_points: 已有的知识点列表
            
        Returns:
            建议的关系列表 [{"target_id": 2, "relation_type": "related", "strength": 0.8, "reason": "..."}]
        """
        if not self.is_available() or not existing_points:
            return []
        
        # 构建已有知识点的简要列表
        points_summary = "\n".join([
            f"{p['id']}. {p['title']}: {p.get('summary', p.get('content', ''))[:100]}"
            for p in existing_points[:20]  # 限制数量避免token过多
        ])
        
        prompt = f"""当前知识点：
标题：{knowledge_point['title']}
内容：{knowledge_point.get('content', '')}

已有知识点：
{points_summary}

请分析当前知识点与已有知识点之间的关系，以JSON格式返回：

关系类型说明：
- prerequisite: 前置知识（需要先学习的）
- related: 相关知识（主题相关）
- extends: 扩展知识（深入或扩展）
- applies_to: 应用场景（可以应用的领域）

返回格式：
[
  {{"target_id": 2, "relation_type": "prerequisite", "strength": 0.9, "reason": "原因说明"}},
  ...
]

只返回强相关的关系（strength > 0.6），最多5个。
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "你是一个知识图谱构建专家。请严格按照JSON格式返回结果。"},
                    {"role": "user", "content": prompt}
                ],
                #temperature=0.6,
                max_completion_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # 清理JSON标记
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            relations = json.loads(content.strip())
            logger.info(f"suggest_knowledge_relations relations: {relations}")
            return relations
        except Exception as e:
            print(f"建议知识关系失败: {str(e)}")
            return []
    
    async def generate_review_question(self, knowledge_point: Dict[str, str]) -> str:
        """
        根据知识点生成复习问题
        
        Args:
            knowledge_point: 知识点信息
            
        Returns:
            生成的复习问题
        """
        if not self.is_available():
            return f"请回顾：{knowledge_point['title']}"
        
        prompt = f"""根据以下知识点生成一个复习问题：

标题：{knowledge_point['title']}
内容：{knowledge_point.get('content', '')}

要求：
1. 问题应该帮助回忆核心概念
2. 可以是简答题、概念解释或应用题
3. 难度适中，能够有效检验理解程度
"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": "你是一个专业的教学设计师。"},
                    {"role": "user", "content": prompt}
                ],
                #temperature=0.8,
                max_completion_tokens=300
            )
            
            result = response.choices[0].message.content.strip()
            logger.info(f"generate_review_question result: {result}")
            return result
        except Exception as e:
            return f"请回顾并解释：{knowledge_point['title']}"


# 创建全局实例
openai_service = OpenAIService()

