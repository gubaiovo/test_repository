# scripts/check.py
"""
Script for Challenge PR Validation

When PR:
- opened/synchronize: validate challenge structure and doc.json
- labeled: recheck when 'recheck' label added

Environ:
- EVENT_TYPE: utilities.EventType
"""

import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, List

sys.path.append(str(Path(__file__).parent.parent))

import gh_cli as gh
from common.log import logger
from utilities import EventType, get_changed

# 校验配置
VALID_DIFFICULTIES = {'Base', 'Normal', 'Hard', 'Other'}
REQUIRED_FIELDS = {
    "author": str,
    "challenge": {
        "difficulty": str,
        "category": str,
        "name": str,
        "introduction": str
    }
}

def validate_doc_structure(doc: dict, path: str) -> List[str]:
    """验证doc.json结构和内容"""
    errors = []
    
    # 必需字段检查
    if "author" not in doc:
        errors.append("Missing required field: author")
    elif not isinstance(doc["author"], str):
        errors.append("author must be a string")
        
    challenge = doc.get("challenge", {})
    if not challenge:
        errors.append("Missing challenge section")
        return errors
        
    for field in ["difficulty", "category", "name", "introduction"]:
        if field not in challenge:
            errors.append(f"Missing challenge field: {field}")
            continue
        if not isinstance(challenge[field], str):
            errors.append(f"{field} must be a string")
    
    # 难度校验
    difficulty = challenge.get("difficulty", "")
    if difficulty not in VALID_DIFFICULTIES:
        errors.append(f"Invalid difficulty: {difficulty}. Valid options: {', '.join(VALID_DIFFICULTIES)}")
    elif difficulty[0].upper() != difficulty[0]:
        errors.append("Difficulty must start with uppercase letter")
    
    # 目录结构校验
    dir_parts = Path(path).parts
    if len(dir_parts) < 2:
        errors.append("Invalid directory structure")
    else:
        # 检查难度目录匹配
        if dir_parts[0] != difficulty:
            errors.append(f"Directory mismatch: {dir_parts[0]} ≠ {difficulty}")
        
        # 检查目录命名
        dir_name = dir_parts[1]
        if ' ' not in dir_name:
            errors.append("Directory name must be [category] name format")
        else:
            category = dir_name.split(' ', 1)[0]
            if category != challenge.get("category", ""):
                errors.append(f"Category mismatch: {category} ≠ {challenge['category']}")
    
    return errors

def validate_doc_json(file_path: Path) -> Dict:
    """验证单个doc.json文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            doc = json.load(f)
    except Exception as e:
        return {"valid": False, "errors": [f"JSON解析错误: {str(e)}"]}
    
    errors = validate_doc_structure(doc, str(file_path.parent))
    return {"valid": len(errors) == 0, "errors": errors}

def main():
    # 获取环境变量
    event_type = EventType(os.environ.get('EVENT_TYPE', ''))
    pr_number = os.environ.get('PR_NUMBER')
    
    # 获取变更文件
    changed_files = get_changed('all_changed_files')
    logger.info(f"Changed files: {changed_files}")
    
    # 只处理doc.json
    doc_files = [
        Path(f) for f in changed_files
        if Path(f).name == "doc.json" and Path(f).parts[0] in VALID_DIFFICULTIES
    ]
    
    # 执行校验
    results = {}
    for doc_path in doc_files:
        results[str(doc_path.parent)] = validate_doc_json(doc_path)
    
    # 生成报告
    report = ["## Challenge Validation Report\n"]
    has_errors = False
    
    for path, result in results.items():
        report.append(f"### `{path}`")
        if result["valid"]:
            report.append("✅ All checks passed")
        else:
            has_errors = True
            report.append("❌ Validation errors:")
            report.extend([f"- {e}" for e in result["errors"]])
        report.append("")
    
    if not results:
        report.append("No doc.json files found in challenge directories")
    
    full_report = '\n'.join(report)
    
    # 更新PR评论
    if event_type in [EventType.OPENED, EventType.SYNCHRONIZE]:
        gh.pr_comment(full_report)
    
    # 如果有错误则失败
    if has_errors:
        logger.error("Validation failed")
        sys.exit(1)
    else:
        logger.info("Validation passed")

if __name__ == "__main__":
    main()