# Changelog

[PyPI History][1]

[1]: https://pypi.org/project/google-cloud-bigtable/#history

## 0.28.1

### Implementation Changes

- Bugfix: Distinguish between an unset column qualifier and an empty string
  column qualifier while parsing a `ReadRows` response (#4252)

### Features added

- Add a ``retry`` strategy that will be used for retry-able errors
  in ``Table.mutate_rows``. This will be used for gRPC errors of type
  ``ABORTED``, ``DEADLINE_EXCEEDED`` and ``SERVICE_UNAVAILABLE``. (#4256)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.1/

## 0.28.0

### Documentation

- Fixed referenced types in `Table.row` docstring (#3934, h/t to
  @MichaelTamm)
- Added link to "Python Development Environment Setup Guide" in
  project README (#4187, h/t to @michaelawyu)

### Dependencies

- Upgrading to `google-cloud-core >= 0.28.0` and adding dependency
  on `google-api-core` (#4221, #4280)

PyPI: https://pypi.org/project/google-cloud-bigtable/0.28.0/
