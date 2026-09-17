from nomad.config.models.plugins import SchemaPackageEntryPoint
from pydantic import Field


class SchemaVisibilityEntryPoint(SchemaPackageEntryPoint):
    allowed_schemas: list[str] | None = Field(
        None,
        description='Schemas that stay available in the "Create new entry" built-in '
        'schema dropdown. Each item is matched against the label shown in the GUI or '
        'the qualified section name. All other schemas are hidden. If not set, '
        'nothing is hidden.',
    )

    def load(self):
        from nomad_oasis_customizer_toolkit.schema_packages.schema_visibility import (
            hide_schemas_not_in,
            m_package,
        )

        if self.allowed_schemas is not None:
            hide_schemas_not_in(self.allowed_schemas, own_entry_point_id=self.id)

        return m_package


schema_visibility = SchemaVisibilityEntryPoint(
    name='Schema visibility',
    description='Hides every built-in and plugin schema that is not allowlisted in '
    'nomad.yaml from the "Create new entry" dialog.',
)
