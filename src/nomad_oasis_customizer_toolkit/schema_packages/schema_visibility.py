from nomad.datamodel.data import EntryData
from nomad.datamodel.metainfo.annotations import SchemaAnnotation
from nomad.metainfo import SchemaPackage

# Holds no definitions; a schema package entry point must return a SchemaPackage.
m_package = SchemaPackage()


def _import_all_schemas(own_entry_point_id: str) -> None:
    """
    Imports everything that nomad.datamodel.all_metainfo_packages imports, so that
    schemas from plugins loaded after this one are hidden as well.
    """
    import nomad.datamodel.metainfo.eln  # noqa: F401
    from nomad.config import config
    from nomad.config.models.plugins import SchemaPackageEntryPoint
    from nomad.parsing.parsers import import_all_parsers

    for entry_point in config.plugins.entry_points.filtered_values():
        if (
            isinstance(entry_point, SchemaPackageEntryPoint)
            and entry_point.id != own_entry_point_id
        ):
            entry_point.load()

    import_all_parsers()


def _entry_data_classes():
    seen = set()
    stack = list(EntryData.__subclasses__())
    while stack:
        cls = stack.pop()
        if cls in seen:
            continue
        seen.add(cls)
        stack.extend(cls.__subclasses__())
        yield cls


def _gui_label(section) -> str:
    # Same fallback order as gui/src/components/uploads/CreateEntry.js
    annotation = section.m_annotations.get('schema')
    if isinstance(annotation, list):
        annotation = annotation[0] if annotation else None
    label = getattr(annotation, 'label', None)
    return label or section.label or section.name


def hide_schemas_not_in(allowed_schemas: list[str], own_entry_point_id: str) -> None:
    """
    Sets SchemaAnnotation(enabled=False) on every EntryData section that is not
    allowlisted. The GUI omits such sections from the built-in schema dropdown; they
    stay fully usable for processing, parsing and existing entries.
    """
    _import_all_schemas(own_entry_point_id)

    allowed = set(allowed_schemas)
    for cls in _entry_data_classes():
        section = cls.m_def
        label = _gui_label(section)
        if label in allowed or section.qualified_name() in allowed:
            continue
        section.m_annotations['schema'] = SchemaAnnotation(label=label, enabled=False)


m_package.__init_metainfo__()
