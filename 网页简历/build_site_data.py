# -*- coding: utf-8 -*-
"""生成网页简历数据源 data.js：从 简历资料/projects.json 提取项目数据 + 个人信息。"""
import io, json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))
PROJ_JSON = os.path.normpath(os.path.join(BASE, "..", "简历资料", "projects.json"))
OUT = os.path.join(BASE, "data.js")

def bullets(content, n=None):
    out = []
    for ln in content.splitlines():
        ln = re.sub(r"^[-*\s]+", "", ln).strip()
        if ln:
            out.append(ln)
    return out[:n] if n else out

def load_projects():
    d = json.load(io.open(PROJ_JSON, encoding="utf-8"))
    projects = []
    for p in d["projects"]:
        sec = {s["heading"]: s["content"] for s in p["sections"]}
        metrics = []
        for ln in bullets(sec.get("关键数据与指标", "")):
            if len(ln) > 4:
                metrics.append(ln)
            if len(metrics) >= 3:
                break
        projects.append({
            "id": p["id"],
            "name": p["name"],
            "category": p["category"],
            "type": p["type"],
            "period": p["period"],
            "org": p["organization"],
            "tags": p["tags"],
            "oneLine": sec.get("一句话简介", "").strip(),
            "background": bullets(sec.get("项目背景（S）", ""), 3),
            "actions": bullets(sec.get("我的职责与动作（A）", ""), 5),
            "results": bullets(sec.get("项目成果（R）", ""), 3),
            "metrics": metrics,
        })
    return projects

def main():
    projects = load_projects()
    personal = {
        "name": "刘洋",
        "title": "产品经理",
        "target": "产品经理",
        "slogan": "水利信息化 · 海外建管数字化",
        "summary": "多项 G 端信息化产品经理经验，主要为工程领域（智慧工地、智慧水利），具备从需求调研→方案设计→原型输出→客户评审演示→用户培训的全流程闭环能力。持有系统集成项目管理工程师（中级）证书，熟悉现场硬件部署与弱电调试场景，有数字孪生模块从数据采集到产品落地的完整经验。曾驻场海外（尼日利亚）全英文协作推进项目，适应高频出差与一线驻场。熟练使用 Axure、Visio、ProcessOn 等原型与流程工具，具备扎实的文档输出与跨团队协调能力。",
        "location": "四川成都",
        "birth": "1997.10",
        "phone": "15680635573",
        "email": "Yangtsegg@163.com",
        "edu": {"school": "成都理工大学", "major": "地理信息科学", "degree": "本科", "period": "2016.09 – 2020.07"},
        "certificates": ["CET-6 · 大学英语六级", "系统集成项目管理工程师（中级）", "工程测量初级职称"],
    }
    # 工作经历：与《刘洋简历-26.9（产品经理）.pdf》保持一致
    work = [
        {"period": "2025.06 – 2026.07", "company": "物知（成都）科技有限公司", "role": "产品经理",
         "project": "尼日利亚某铁路现代化项目，涉及智慧工地系统（劳务管理、物资管理、安质管理、搅拌站系统等模块）的售前支持与产品落地。",
         "points": [
            "需求调研与方案设计：深入铁路施工现场，独立调研中方施工单位与尼方监理单位的业务痛点，确定技术指标与功能边界，完成成本估算及风险预案，输出完整解决方案并通过客户评审",
            "产品演示与售前转化：针对智慧工地各核心模块制作演示原型与讲解材料，配合完成多轮客户演示，支撑项目售前转化",
            "基础客服助手验证：根据现场安质管理痛点，整理项目制度文档与施工案例构建初级知识库，利用企业微信搭建客服助手",
            "空间数据产品化：驻场期间独立完成铁路施工现场及航站楼无人机航拍数据采集，生成正射影像底图交付 BIM 团队，辅助建模与空间展示，理解从数据采集到业务应用的完整链路",
            "硬件现场协调：参与现场弱电硬件安装调试，了解工业摄像头、传感器等设备的部署条件与现场约束，能在产品设计中预判硬件兼容性风险",
            "跨团队推进：协调中方施工方、尼方监理、内部技术团队多方沟通，跟进系统运行反馈，推动需求迭代"]},
        {"period": "2024.04 – 2025.04", "company": "四川星海数创科技有限公司", "role": "产品经理",
         "project": "灌区水利运行管理信息化系统，面向多个灌区客户提供售前方案与产品落地支持。",
         "points": [
            "售前方案体系化：独立完成灌区信息化需求调研与方案设计，编制技术方案文档，建立并迭代灌区水利解决方案模板库，提升方案设计效率与精准度，支撑多个灌区项目售前转化",
            "数字孪生模块全流程：主导数字孪生模块的产品落地——从无人机航拍数据采集、正射影像生成、三维实景建模到数据质检与成果交付，理解空间数据如何支撑业务一张图等可视化产品需求",
            "客户对接与需求管理：对接业主与第三方硬件厂商，协调内部技术、实施团队解决项目筹备中的技术疑问与需求变更，维护核心客户关系并推动二次合作",
            "培训与交付：编写标准用户手册，负责售后用户培训，确保最终用户能独立操作系统"]},
        {"period": "2021.12 – 2024.03", "company": "成都市赛零信息技术开发有限公司", "role": "产品经理",
         "project": "区县水利信息化项目（泸县、纳溪区、隆昌市等），涵盖水利一张图、工程一张图等核心模块。",
         "points": [
            "多项目并行交付：独立负责多个区县级客户的需求调研、方案设计与评审演示，输出需求规格说明书、用户手册及配套原型，客户满意度高",
            "GIS 产品化落地：规划并推进 GIS 功能在业务应用层面的产品化——完成水利一张图、工程一张图等核心模块的需求定义与迭代设计，将空间数据能力转化为可交付的产品功能",
            "数字孪生支撑：负责无人机航拍数据预处理、影像拼接、正射校正及三维模型构建，为水利项目的数字孪生展示需求提供数据与模型基础"]},
        {"period": "2020.07 – 2021.12", "company": "香港科纳海洋工程有限公司", "role": "导航工程师",
         "project": "驻场中石油某海外海洋勘探船队，负责海洋设备的运行维护与勘探路径规划。",
         "points": [
            "综合导航系统操作：熟练操作综合导航系统（Dolphin、海经等），负责海上地震勘探作业（OBC/OBN）的测线导航、节点布放及震源激发控制，确保定位精度达厘米级、时间同步精度达微秒级",
            "多船协同与作业调度：在复杂海况下负责震源船、节点船及声学定位船的多船协同作业调度，动态调整作业参数与布放路径，保障船队生产计划的连贯性与作业日效",
            "水下声学定位与质控：操作长基线 / 超短基线（USBL）声学定位系统，实时追踪水下节点 / 电缆位置；负责现场导航数据的实时监控与异常排查，确保勘探数据的高质量采集",
            "设备动态校验与应急排障：执行导航定位设备（GNSS、罗经、测深仪等）的动态校验与日常维护，具备快速响应与现场故障排除能力，保障导航系统“零差错”运行"]},
    ]
    evaluation = [
        {"title": "专业力", "desc": "多项 G 端信息化产品经理经验，聚焦工程领域（智慧工地、智慧水利），覆盖“需求调研 → 方案设计 → 原型输出 → 客户评审演示 → 用户培训”全流程闭环。"},
        {"title": "执行力", "desc": "具备数字孪生模块从无人机航拍数据采集、正射影像生成、三维建模到成果交付的完整经验，熟悉现场硬件部署与弱电调试场景。"},
        {"title": "适应力", "desc": "曾驻场海外（尼日利亚）全英文协作推进项目，适应高频出差与一线驻场；持系统集成项目管理工程师（中级）证书。"},
    ]
    abilities = [
        {"group": "产品专业", "items": ["需求调研与管理", "方案设计与成本估算", "Axure 高保真原型", "HTML 高保真原型", "Visio / ProcessOn 流程设计", "版本迭代规划"]},
        {"group": "业务领域", "items": ["水利信息化", "灌区管理", "智慧水务", "海外建管/智慧工地", "数字孪生", "GIS 应用", "物联网/软硬一体"]},
        {"group": "交付协作", "items": ["售前方案与演示", "第三方厂商对接", "驻场实施协调", "用户培训与手册", "监理/咨询方协同", "跨文化沟通"]},
    ]
    stats = [
        {"num": "5+", "label": "年产品经验"},
        {"num": "12", "label": "项项目作品"},
        {"num": "4", "label": "大业务板块"},
        {"num": "2", "label": "次海外驻场"},
    ]
    data = {
        "personal": personal,
        "stats": stats,
        "evaluation": evaluation,
        "work": work,
        "projects": projects,
        "abilities": abilities,
        "updated": "2026-08",
    }
    js = "/* 自动生成：由 build_site_data.py 从 简历资料/projects.json 生成。请勿手改，修改后重跑脚本。 */\n"
    js += "window.PM_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n"
    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write(js)
    print("OK ->", OUT, "| projects:", len(projects))

if __name__ == "__main__":
    main()