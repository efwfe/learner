"""
遗忘曲线算法实现 - 基于 SuperMemo SM-2 算法
该算法根据复习质量动态调整复习间隔
"""
from datetime import datetime, timedelta
from typing import Tuple


class SpacedRepetitionAlgorithm:
    """间隔重复算法（SuperMemo SM-2）"""
    
    @staticmethod
    def calculate_next_review(
        quality: int,
        ease_factor: float,
        interval: int,
        repetitions: int
    ) -> Tuple[float, int, int, datetime]:
        """
        计算下次复习时间
        
        Args:
            quality: 复习质量评分 (0-5)
                0: 完全不记得
                1: 错误答案
                2: 错误但想起来了
                3: 困难但正确
                4: 犹豫后正确
                5: 完美记忆
            ease_factor: 难易度因子 (初始值 2.5)
            interval: 当前间隔天数
            repetitions: 重复次数
            
        Returns:
            (新的ease_factor, 新的interval, 新的repetitions, 下次复习日期)
        """
        # 确保 quality 在有效范围内
        quality = max(0, min(5, quality))
        
        # 计算新的难易度因子
        new_ease_factor = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # 难易度因子不能低于 1.3
        new_ease_factor = max(1.3, new_ease_factor)
        
        # 根据质量决定是否增加重复次数
        if quality < 3:
            # 如果质量差，重置重复次数和间隔
            new_repetitions = 0
            new_interval = 1
        else:
            new_repetitions = repetitions + 1
            
            # 根据重复次数计算新间隔
            if new_repetitions == 1:
                new_interval = 1
            elif new_repetitions == 2:
                new_interval = 6
            else:
                new_interval = round(interval * new_ease_factor)
        
        # 计算下次复习日期
        next_review_date = datetime.utcnow() + timedelta(days=new_interval)
        
        return new_ease_factor, new_interval, new_repetitions, next_review_date
    
    @staticmethod
    def get_priority_level(next_review_date: datetime, ease_factor: float) -> str:
        """
        获取复习优先级
        
        Args:
            next_review_date: 下次复习日期
            ease_factor: 难易度因子
            
        Returns:
            优先级: "high", "medium", "low"
        """
        days_until_review = (next_review_date - datetime.utcnow()).days
        
        # 已逾期或今天需要复习
        if days_until_review <= 0:
            return "high"
        # 难易度因子低（困难）且即将需要复习
        elif ease_factor < 2.0 and days_until_review <= 2:
            return "high"
        # 未来1-3天需要复习
        elif days_until_review <= 3:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def estimate_review_time(repetitions: int, ease_factor: float) -> int:
        """
        估算复习时间（分钟）
        
        Args:
            repetitions: 重复次数
            ease_factor: 难易度因子
            
        Returns:
            预估时间（分钟）
        """
        # 基础时间：5分钟
        base_time = 5
        
        # 根据重复次数减少时间（熟练度提高）
        time_reduction = min(repetitions * 0.5, 3)
        
        # 根据难易度因子调整时间
        difficulty_factor = 3.0 - ease_factor  # 越困难花费时间越多
        difficulty_adjustment = max(0, difficulty_factor * 2)
        
        estimated_time = base_time - time_reduction + difficulty_adjustment
        
        return max(2, round(estimated_time))  # 最少2分钟

