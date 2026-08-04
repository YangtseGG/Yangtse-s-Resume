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
        "summary": "5 年 B/G 端软件产品经验：从需求调研、功能设计、高保真原型到驻场交付与版本迭代，完成 12 个信息化项目的全链路落地，覆盖水利、水务、灌区与海外建管四大板块。",
        "location": "四川成都",
        "birth": "1997.10",
        "phone": "15680635573",
        "email": "Yangtsegg@163.com",
        "edu": {"school": "成都理工大学", "major": "地理信息科学", "degree": "本科", "period": "2016.09 – 2020.07"},
        "certificates": ["CET-6 · 大学英语六级", "系统集成项目管理工程师（中级）", "工程测量初级职称"],
    }
    work = [
        {"period": "2025.06 – 2026.07", "company": "物知（成都）科技有限公司", "role": "产品经理", "points": [
            "负责尼日利亚某铁路现代化项目智慧工地系统：软件需求、功能设计、版本迭代与验收材料编写",
            "驻场尼日利亚，协调中方施工单位与尼方监理单位，推进项目实施并跟进系统运行反馈",
            "参与现场弱电硬件安装调试；协助售前补充投标材料中软件功能与架构内容"]},
        {"period": "2024.04 – 2025.04", "company": "四川星海数创科技有限公司", "role": "产品经理", "points": [
            "负责灌区水利运行管理信息化系统：需求管理、功能设计、模块迭代计划",
            "对接业主与第三方硬件厂商；配合售前完成系统演示汇报与解决方案编写",
            "负责售后：上线后用户培训与标准用户手册编写"]},
        {"period": "2021.12 – 2024.03", "company": "成都市赛零信息技术开发有限公司", "role": "产品经理", "points": [
            "负责区县水利单位客户的水利信息化系统，完成 5+ 项目交付，累计服务 3 个区县级客户",
            "部分项目兼任项目助理：跟进项目进度、对接第三方厂商、补充完善验收材料",
            "负责公司内部数字孪生与 GIS 功能在业务应用方面的规划"]},
        {"period": "2020.07 – 2021.11", "company": "深圳市国力昂科技有限公司", "role": "产品助理", "points": [
            "协助海洋导航勘探软件迭代：需求收集与用户反馈收集",
            "外驻中石油海外船队跟进产品落地"]},
    ]
    evaluation = [
        {"title": "专业力", "desc": "经历并交付多项不同精细度的软件信息化项目，业主涉及不同企事业单位，覆盖政务、水务与海外工程场景。"},
        {"title": "执行力", "desc": "较强的责任心与自我驱动力，多次跨团队协作经验，推动复杂项目从调研到落地交付。"},
        {"title": "适应力", "desc": "接受高频出差，具备一线驻场经验，能与外方业主用英语进行日常沟通。"},
    ]
    abilities = [
        {"group": "产品专业", "items": ["需求调研与管理", "功能设计", "Axure 高保真原型", "HTML 高保真原型", "版本迭代规划", "验收材料编写"]},
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