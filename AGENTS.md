# Conformance lab operating contract

- Keep `main` free of intentionally unsafe fixtures.
- Put each adversarial case on its own short-lived branch and pull request.
- Never add secrets, customer data, production endpoints, or deploy credentials.
- Expected `DENY` and pre-model rejection runs are successful test evidence even
  though the GitHub check conclusion is failure.
- Do not activate or edit organization rulesets from this repository.
