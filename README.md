# nomad-oasis-customizer-toolkit

A NOMAD plugin with tools for customizing a NOMAD Oasis through `nomad.yaml`, without
changing NOMAD or its GUI. Each tool is a separate entry point that does nothing until it
is configured.

## Schema visibility

Limits the schemas offered for creating new entries to an allowlist, in both the classic
GUI (*Create new entry* dialog) and the new GUI (v2).

### Why not `plugins.entry_points.exclude`

Most of the dropdown (Basic ELN, Instrument ELN, Workflows, ...) is defined inside the
`nomad-lab` package itself and is imported unconditionally, not through plugin entry
points. NOMAD also force-loads some schema plugins (e.g. `simulationworkflowschema`)
whenever they are installed. `exclude` can therefore not remove them from the dropdown.

### How it works

When NOMAD loads schema plugins at startup, this entry point imports all other schemas and
sets NOMAD's documented `SchemaAnnotation(enabled=False)` on every `EntryData` section
that is not allowlisted. The GUI omits such sections from the dropdown.

Hidden schemas stay fully functional: parsing, processing, search and existing entries
are unaffected, and definition ids do not change. Hiding is not access control; entries
of a hidden schema can still be created by uploading files.

### Configuration

```yaml
plugins:
  entry_points:
    options:
      nomad_oasis_customizer_toolkit.schema_packages:schema_visibility:
        allowed_schemas:
          - TrainingResource
          - Event Participation Request
          - FAIRmat PI Onboarding
```

Each item is matched against the schema's labels (as shown in the classic GUI or the new
GUI v2), its name, or its qualified section name
(e.g. `nomad.datamodel.metainfo.eln.ELNSample`). Without `allowed_schemas` nothing is
hidden. Restart the app after changing the list.
