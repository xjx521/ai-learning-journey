### Day 19：类型注解、dataclass

#### 题目 1：类型注解 ⭐⭐


def process_student(name: str, age: int, scores: list[float]) -> dict:
    return {
        "name": name,
        "age": age,
        "scores": scores,
        "average": sum(scores) / len(scores) if scores else 0,
    }
