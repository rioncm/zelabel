"""Household label definitions in 203 dpi dot coordinates."""


def field(id, label, placeholder, x, y, width, font, *, limit=48, lines=1, required=False, checkbox=False):
    return dict(id=id, label=label, placeholder=placeholder, x=x, y=y,
                width=width, font=font, limit=limit, lines=lines,
                required=required, checkbox=checkbox)


TEMPLATES = {
    "storage-box": dict(name="Storage box", category="Organize", size="4×2", width=812, height=406,
        description="A bold title, contents, and location.", fields=[
            field("title", "Box title", "Winter decorations", 42, 36, 728, 58, limit=36, lines=2, required=True),
            field("contents", "What's inside", "Lights, ornaments, hooks", 42, 188, 728, 32, limit=90, lines=3),
            field("location", "Stored in", "Garage, shelf 2", 42, 347, 728, 24, limit=42),
        ]),
    "jar-can": dict(name="Jar or can", category="Kitchen", size="2×2", width=406, height=406,
        description="Contents, date, and a short note.", fields=[
            field("contents", "Contents", "Peach jam", 28, 42, 350, 46, limit=22, lines=2, required=True),
            field("date", "Date", "2026-09-26", 28, 224, 350, 29, limit=18),
            field("note", "Note", "Use by spring", 28, 301, 350, 23, limit=42, lines=2),
        ]),
    "todo-list": dict(name="To do list", category="Planning", size="4×2", width=812, height=406,
        description="A title with four short tasks.", fields=[
            field("title", "List title", "Weekend jobs", 42, 29, 728, 42, limit=27, required=True),
            *[field(f"item{n}", f"Task {n}", "Add a task", 82, 103+(n-1)*68, 680, 30, limit=35, checkbox=True) for n in range(1, 5)],
        ]),
    "project-card": dict(name="Project card", category="Planning", size="4×2", width=812, height=406,
        description="A Kanban card with the next step and owner.", fields=[
            field("project", "Project", "Pantry refresh", 42, 30, 728, 40, limit=28, required=True),
            field("task", "Next step", "Sort the upper shelves", 42, 121, 728, 36, limit=62, lines=2, required=True),
            field("owner", "Owner", "Rion", 42, 312, 340, 25, limit=21),
            field("status", "Stage", "NEXT", 450, 312, 320, 25, limit=20),
        ]),
}


def public_templates():
    """Expose form metadata without internal layout coordinates."""
    return [{"id": key, "name": item["name"], "category": item["category"],
             "size": item["size"], "description": item["description"],
             "fields": [{"id": f["id"], "label": f["label"], "placeholder": f["placeholder"],
                         "maxLength": f["limit"], "required": f["required"]} for f in item["fields"]]}
            for key, item in TEMPLATES.items()]
