# CHANGELOG

<!-- version list -->

## v2.6.0 (2025-07-22)

### Features

- Attr source fields
  ([`e9c626b`](https://github.com/janthmueller/swizzle/commit/e9c626b93aa5751477541d4084a24e7e0b4eec68))


## v2.5.2 (2025-07-15)

### Bug Fixes

- Only_attrs can be empty sequence
  ([`fae2cdb`](https://github.com/janthmueller/swizzle/commit/fae2cdb6b8c248038e2253e17fe466ab64c9e559))


## v2.5.1 (2025-07-14)

### Bug Fixes

- Use same defaults as module call
  ([`b8d92d3`](https://github.com/janthmueller/swizzle/commit/b8d92d3419a82447fd07448bd056c0322e8a5198))

### Chores

- Ignore docs
  ([`1fa6b84`](https://github.com/janthmueller/swizzle/commit/1fa6b84084d6f427f4ad46ebbe91d618be2c86f4))

### Documentation

- Fix typo
  ([`290af1f`](https://github.com/janthmueller/swizzle/commit/290af1f879bdb44380f7bc12114307efd83c565c))

### Refactoring

- Helper functions to utils
  ([`812deca`](https://github.com/janthmueller/swizzle/commit/812decaf6cfa9080c99da5d51bb2c82a5c2cd4ac))


## v2.5.0 (2025-07-13)

### Bug Fixes

- Rework sep logic
  ([`19b297e`](https://github.com/janthmueller/swizzle/commit/19b297ec55943c890c0157be939fc06c4ba91b93))

### Chores

- Update readme
  ([`23fd06c`](https://github.com/janthmueller/swizzle/commit/23fd06c1bbdca7efbfd3e030e6a1d8fa339d9771))

### Documentation

- Review-later
  ([`e506197`](https://github.com/janthmueller/swizzle/commit/e506197252c04bd3afa9ef79dcc6c63701ebc4cc))

### Features

- Return trie arg - reuse trie in setter
  ([`eb21a11`](https://github.com/janthmueller/swizzle/commit/eb21a11e9a7add4428b55b48e0c55bb3ba735c41))

- Setter
  ([`857173b`](https://github.com/janthmueller/swizzle/commit/857173b61d69b40befd9a8574ece2d5e1b0d4f38))

- Setter, only-attrs from slots or dir
  ([`ea36e50`](https://github.com/janthmueller/swizzle/commit/ea36e5019363f57a90d1dfb902567be387981899))

- Whitelist swizzle attr name length with only_attrs
  ([`04f77e3`](https://github.com/janthmueller/swizzle/commit/04f77e3e3341b7c2eefb81d5329a70b0e103e6b9))

### Performance Improvements

- Use slots on trie node
  ([`0369dc3`](https://github.com/janthmueller/swizzle/commit/0369dc39e95cb9dbdc863ef06ecc48cd156c1b75))

### Refactoring

- Changed verror to aerror
  ([`2951e9e`](https://github.com/janthmueller/swizzle/commit/2951e9e747b19e46f57d9e2a4da539a967660862))

- Comments and formatting
  ([`3da8d37`](https://github.com/janthmueller/swizzle/commit/3da8d374df66ec80b66ce358c98bb2102e45bacc))

- Remove prints
  ([`1aa451e`](https://github.com/janthmueller/swizzle/commit/1aa451e6f85bb1460bc208e60e7f07553521792d))

- Rename and chunk functions
  ([`3e5bd04`](https://github.com/janthmueller/swizzle/commit/3e5bd04c9e43cfb9cd4361462f71adef757b7e26))

- Rename to differentiate between getter/setter
  ([`82bd8b0`](https://github.com/janthmueller/swizzle/commit/82bd8b0def6f6133d0f9cbbd6c955af8a56bd382))


## v2.4.0 (2025-06-29)

### Continuous Integration

- **test**: Run on all branches
  ([`a0b2e84`](https://github.com/janthmueller/swizzle/commit/a0b2e84a4d6d24100d451291f55290e066d42110))

### Documentation

- **readme**: Swizzle.t = swizzledtuple
  ([`fa087d0`](https://github.com/janthmueller/swizzle/commit/fa087d073eeb786a7d55c13c2cd94ae3b601eeb1))

### Features

- **swizzledtuple**: Arg arrange_name as positional
  ([`af7abea`](https://github.com/janthmueller/swizzle/commit/af7abeab5b6357ebf5ce7f587b39a39e57867af4))

### Refactoring

- **swizzledtuple**: Removed unused _map
  ([`a5e4313`](https://github.com/janthmueller/swizzle/commit/a5e431398e9c725f5b046dc6acdc2951edef9dc6))


## v2.3.6 (2025-06-29)

### Bug Fixes

- Trigger full release
  ([`8cf10a7`](https://github.com/janthmueller/swizzle/commit/8cf10a7e6ca744caab9aca0980c02ef4072360b8))


## v2.3.5 (2025-06-29)

### Bug Fixes

- **semantic-release**: Repository instead pypi
  ([`70f0800`](https://github.com/janthmueller/swizzle/commit/70f0800a9eb39a3ed4cffd9f0b334276dc128c07))


## v2.3.4 (2025-06-29)

### Bug Fixes

- Trigger release
  ([`9073887`](https://github.com/janthmueller/swizzle/commit/9073887bfca3457ce9b56adc7116c3f437e0a552))


## v2.3.3 (2025-06-29)

### Bug Fixes

- _check_for_existing_members_ only on 3.11+
  ([`093642b`](https://github.com/janthmueller/swizzle/commit/093642b56426c4880c1a81f9ddfe3a63ec66ef07))

- Back to 3.11+ for enum
  ([`a1946e9`](https://github.com/janthmueller/swizzle/commit/a1946e939260bc2151ef7204960626ac3131d81b))

- Cfem name follow up / missed old getattr
  ([`21a3e48`](https://github.com/janthmueller/swizzle/commit/21a3e4874fc22ff7f745290de206889ec5793403))

- Ci
  ([`40f8a26`](https://github.com/janthmueller/swizzle/commit/40f8a263392e0f81f215b2602f74ed42af9282ed))

- Different cfem_names on different versions
  ([`eea1600`](https://github.com/janthmueller/swizzle/commit/eea16004d4729a032fed14e59f60a202193da01a))

- Pypi secret token name
  ([`0f64d3f`](https://github.com/janthmueller/swizzle/commit/0f64d3fec58c1bfa28e9c073edc9bb1f98da5c91))

- Replace EnumType with EnumMeta for Python < 3.11 compatibility
  ([`9ab25f1`](https://github.com/janthmueller/swizzle/commit/9ab25f1408e9edef0c15ebbc2bd07cb04f47337f))

- Skip metaclass enum tests for Python < 3.11
  ([`f498f99`](https://github.com/janthmueller/swizzle/commit/f498f9978e0fa7bc5b82447c5c2c8c224a92c649))

- Skip metaclass enum tests for Python < 3.11
  ([`3a67b31`](https://github.com/janthmueller/swizzle/commit/3a67b31418ef0da0264de7ab0fe2c937b117c6c4))

- Trigger patch release
  ([`092a1d8`](https://github.com/janthmueller/swizzle/commit/092a1d8b19c116b2cb3cfaaaa715f74cae3cf56c))

- Versioning
  ([`42dd131`](https://github.com/janthmueller/swizzle/commit/42dd131798c80aa2c1d4e45666b42aae58f6889b))

### Chores

- Add commit linting config
  ([`6b038ca`](https://github.com/janthmueller/swizzle/commit/6b038ca7149d4374a718516c175d9a9307220a7d))

- Drop support for Python 3.6
  ([`d7e3434`](https://github.com/janthmueller/swizzle/commit/d7e343438d2a384e5228b3592381d26fca690d41))

- Drop support for python 3.7
  ([`dff9493`](https://github.com/janthmueller/swizzle/commit/dff94934e49e2399b4f31baf9e618d654f541117))

### Continuous Integration

- Major rework
  ([`6585df3`](https://github.com/janthmueller/swizzle/commit/6585df3806b75a1b102a2922103d5b70adef4de2))

- No release upload
  ([`3036439`](https://github.com/janthmueller/swizzle/commit/30364398f96656aea2a8c085b9f5111cbe7d6d26))

- Update test
  ([`0f77cde`](https://github.com/janthmueller/swizzle/commit/0f77cde3884fe816dc9551e9537cf090fed54524))

- **release**: Manual trigger
  ([`1875e50`](https://github.com/janthmueller/swizzle/commit/1875e50527ca84b1759b3224188750a407eb2ee6))

- **workflow**: Fail no release
  ([`2a5e701`](https://github.com/janthmueller/swizzle/commit/2a5e70193ab6d24b3f4a56627fe4f9b7708ec655))

### Refactoring

- Removed unnecessary function calls
  ([`916cfb3`](https://github.com/janthmueller/swizzle/commit/916cfb3d1e364338519024d2d6d42ab2091ec04b))


## v2.3.2 (2025-06-29)


## v2.3.1 (2025-06-29)


## v2.3.0 (2025-06-29)


## v2.2.1 (2025-06-29)


## v2.2.0 (2025-06-29)

### Refactoring

- Unsupport old arg names, use sep, fixed missing error on sep
  ([`074a6d1`](https://github.com/janthmueller/swizzle/commit/074a6d1f1a1aeb97066584f520999cff9370bc6f))


## v2.1.1 (2025-06-29)

### Chores

- Remove unwanted print; bump version to 2.1.1
  ([`57c45d8`](https://github.com/janthmueller/swizzle/commit/57c45d8f91c567c6a7c0bf304d3f89d606c31eb7))


## v2.1.0 (2025-06-29)


## v2.0.0 (2025-06-29)

### Chores

- Update README.md with badges and links
  ([`5f4f59a`](https://github.com/janthmueller/swizzle/commit/5f4f59a50c5d011a78f71989d4046de8a5b7656f))


## v1.0.0 (2025-06-29)


## v0.1.4 (2025-06-29)


## v0.1.3 (2025-06-29)


## v0.1.2 (2025-06-29)


## v0.1.0 (2025-06-29)

- Initial Release
