from nomad.datamodel.metainfo.eln import BasicEln, ELNInstrument, ELNSample

from nomad_oasis_customizer_toolkit.schema_packages.schema_visibility import (
    hide_schemas_not_in,
)

ENTRY_POINT_ID = 'nomad_oasis_customizer_toolkit.schema_packages:schema_visibility'


def is_enabled(section) -> bool:
    annotation = section.m_annotations.get('schema')
    if isinstance(annotation, list):
        annotation = annotation[0] if annotation else None
    return getattr(annotation, 'enabled', True)


def test_only_allowlisted_schemas_stay_enabled():
    hide_schemas_not_in(
        ['Basic ELN', 'nomad.datamodel.metainfo.eln.ELNSample'],
        own_entry_point_id=ENTRY_POINT_ID,
    )

    assert is_enabled(BasicEln.m_def)  # matched by GUI label
    assert is_enabled(ELNSample.m_def)  # matched by qualified name
    assert not is_enabled(ELNInstrument.m_def)
    assert ELNInstrument.m_def.m_annotations['schema'].label == 'Instrument ELN'
