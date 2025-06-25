# Pronoun and Title Usage Guide for Personalities

## Overview

The personality system includes a comprehensive pronoun and title system that allows you to configure how the AI addresses the user and how the user should address the AI. This creates more immersive and personalized roleplay experiences.

## Pronoun Configuration Fields

### User-Focused Pronouns (How AI addresses the user)

```json
"pronouns": {
  "user_title": "sir",           // Formal title (e.g., "sir", "madam", "captain", "doctor")
  "user_name": "Bob",            // User's preferred name
  "user_pronouns": "he/him",     // User's preferred pronouns
  "user_formal": false           // Whether to use formal address
}
```

### AI/Character Pronouns (How AI refers to itself)

```json
"pronouns": {
  "character_name": "Father",    // AI's character name
  "character_title": "Your Father", // AI's character title
  "gender": "male"               // AI's gender for pronoun selection
}
```

## Common Usage Patterns

### 1. Family Relationships

**Father-Son (like our updated father.json):**
```json
{
  "user_name": "Bob",
  "user_pronouns": "he/him",
  "user_formal": false,
  "character_name": "Father",
  "character_title": "Your Father",
  "gender": "male"
}
```

**Mother-Daughter:**
```json
{
  "user_name": "Sarah",
  "user_pronouns": "she/her",
  "user_formal": false,
  "character_name": "Mother",
  "character_title": "Your Mother",
  "gender": "female"
}
```

### 2. Professional Relationships

**Boss-Employee:**
```json
{
  "user_title": "Mr. Johnson",
  "user_name": "Johnson",
  "user_pronouns": "he/him",
  "user_formal": true,
  "character_name": "Boss",
  "character_title": "Your Manager",
  "gender": "neutral"
}
```

**Teacher-Student:**
```json
{
  "user_name": "Alex",
  "user_pronouns": "they/them",
  "user_formal": false,
  "character_name": "Professor Smith",
  "character_title": "Your Teacher",
  "gender": "neutral"
}
```

### 3. Roleplay Scenarios

**Knight-Squire:**
```json
{
  "user_name": "Squire",
  "user_pronouns": "he/him",
  "user_formal": true,
  "character_name": "Sir Galahad",
  "character_title": "Your Knight",
  "gender": "male"
}
```

**Wizard-Apprentice:**
```json
{
  "user_name": "Apprentice",
  "user_pronouns": "they/them",
  "user_formal": false,
  "character_name": "Master Merlin",
  "character_title": "Your Master",
  "gender": "male"
}
```

## Template Placeholders

The system supports these placeholders in prompts and templates:

- `{user}` - Gets the appropriate user address (name, title, or "you")
- `{user_name}` - User's name
- `{user_title}` - User's title
- `{user_pronouns}` - User's pronouns

### Example Usage in Templates

```json
{
  "user_prompt_template": "{user_name}: {user_input}\n{character_name}:",
  "context_prompt": "Previous conversation with {user_name}:\n{context}\n\n{user_name} says: {user_input}"
}
```

## Best Practices

### 1. Choose Appropriate Pronouns
- Use `he/him` for male users
- Use `she/her` for female users  
- Use `they/them` for non-binary users or when gender is unknown
- Use `they/them` for general/neutral addressing

### 2. Formal vs Informal
- Set `user_formal: true` for professional, hierarchical, or respectful relationships
- Set `user_formal: false` for casual, friendly, or family relationships

### 3. Names and Titles
- Use `user_name` for personal relationships (family, friends)
- Use `user_title` for formal relationships (boss, teacher, military)
- Leave both empty for generic addressing

### 4. Character Configuration
- `character_name` should be how the AI thinks of itself
- `character_title` should be how the AI introduces itself to the user
- `gender` affects how the AI refers to itself in third person

## Example: Complete Father Personality

```json
{
  "pronouns": {
    "user_title": "",
    "user_name": "Bob",
    "user_pronouns": "he/him",
    "user_formal": false,
    "character_name": "Father",
    "character_title": "Your Father",
    "gender": "male"
  }
}
```

This configuration tells the AI:
- Address the user as "Bob" (personal name)
- Use "he/him" pronouns when referring to Bob
- Use informal/casual address (no formal titles)
- Think of itself as "Father"
- Introduce itself as "Your Father"
- Use male pronouns when referring to itself

## Testing Your Configuration

To test if your pronoun configuration is working:

1. Load the personality in the app
2. Send a message like "Hello, how are you?"
3. Check if the AI uses the correct name and pronouns
4. Try asking "What's my name?" to see how the AI refers to you

## Common Issues and Solutions

### Issue: AI not using the user's name
**Solution:** Make sure `user_name` is set and the system prompt mentions using the name

### Issue: AI using wrong pronouns
**Solution:** Check that `user_pronouns` is set correctly and the system prompt includes pronoun guidance

### Issue: AI being too formal/informal
**Solution:** Adjust `user_formal` setting and update the system prompt tone accordingly

### Issue: Templates not working
**Solution:** Ensure you're using the correct placeholder syntax: `{user_name}`, `{user_title}`, etc. 