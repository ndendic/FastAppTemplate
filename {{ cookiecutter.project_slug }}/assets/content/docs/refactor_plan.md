### Areas for Refactoring

1. UI Component Separation
- Table components are mixed with data handling
- Modal form logic could be more modular
- Rendering factories could be separated

2. Code Duplication
- Similar rendering logic in multiple places
- Repeated field processing
- Common UI patterns that could be abstracted

3. Complex Methods
- Large methods like form_data() and _dict_with_custom_encoder()
- Nested functionality in ModelTableFromDicts
- Complex field type handling

4. Configuration Management
- Scattered field definitions
- Multiple places handling field attributes
- UI-specific configs mixed with model definitions