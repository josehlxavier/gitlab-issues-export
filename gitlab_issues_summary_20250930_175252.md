# Relatório Resumido - Issues do GitLab

**Data da extração:** 2025-09-30 17:52:52
**Total de issues:** 16
**Projeto:** raidiam-conformance/open-finance/certification

## 📊 Estatísticas Gerais

### Por Estado
- **Opened:** 16 issues

### Top Autores
- **Carla Moreno:** 2 issues
- **Rafael de Freitas Cassalichio:** 2 issues
- **Caio Tranjan:** 1 issues
- **Matheus Mantovani:** 1 issues
- **Gutemberg Cedraz:** 1 issues
- **Patrick Hadson:** 1 issues
- **Bruno Pacheco:** 1 issues
- **rodrigomagnos1:** 1 issues
- **Eri Silva:** 1 issues
- **João P Oliveira:** 1 issues

### Labels Mais Comuns
- **Automatic Payments::v2:** 9 issues
- **Conformance Suite:** 7 issues
- **Change Request:** 5 issues
- **GT Serviços:** 5 issues
- **FVP:** 5 issues
- **Under WG/DTO Evaluation:** 4 issues
- **Backlog:** 4 issues
- **Bug:** 3 issues
- **In progress:** 3 issues
- **Questions:** 3 issues
- **Waiting Participant:** 2 issues
- **Under Evaluation:** 2 issues
- **Payments :: v4:** 2 issues
- **Mock Bank:** 1 issues
- **No Redirect Payments :: v2:** 1 issues

## 📋 Lista Detalhada das Issues

### 1. Issue #2348

**📌 Título:** enrollments_automatic-payments_sweeping-consent-not-authorised_v2-2 – Non existent Error resons for 422 FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO

**👤 Autor:** Caio Tranjan (@caio.tranjan)
**📅 Criado:** 2025-09-30 às 18:24:46
**🔄 Atualizado:** 2025-09-30 às 19:09:20
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2348
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Change Request, GT Serviços, Under WG/DTO Evaluation

**📝 Descrição:** Test Module was implemented following defined in: 'RAD-203'  Behavior:  enrollments_automatic-payments_sweeping-consent-not-authorised_v2-2  Test module summary:  <table> <tr> <th>  **Ensure a recurri...

---

### 2. Issue #2347

**📌 Título:** PCM Failure on GET private/report - OCS-160

**👤 Autor:** Matheus Mantovani (@matheus-mantovani)
**📅 Criado:** 2025-09-30 às 17:30:09
**🔄 Atualizado:** 2025-09-30 às 17:40:40
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2347
**⚡ Estado:** OPENED
**🏷️ Labels:** Backlog, Change Request, FVP

**📝 Descrição:** **Observed Behavior:**  PCM Fetch Logs endpoint  * GET `/report-api/v1/private/report/{fapiInteractionId}`  Fails to fetch reports, receiving error 401 from PCM.  Current FVP PCM integration was imple...

---

### 3. Issue #2346

**📌 Título:** Inconsistency in DCR generation – software_statement with invalid date

**👤 Autor:** Gutemberg Cedraz (@GutembergTeros)
**📅 Criado:** 2025-09-30 às 15:59:11
**🔄 Atualizado:** 2025-09-30 às 16:48:08
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2346
**⚡ Estado:** OPENED
**🏷️ Labels:** FVP, Waiting Participant
**📈 Estatísticas:** 💬 1 comentários

**📝 Descrição:** During the registration/integration flow, the test engine issues the software_statement with an iat/date earlier than the current time, violating the requirement to issue with a valid, present timesta...

---

### 4. Issue #2345

**📌 Título:** Rejected consent at redirection missing rejection object

**👤 Autor:** Carla Moreno (@carla-raidiam)
**📅 Criado:** 2025-09-30 às 13:05:42
**🔄 Atualizado:** 2025-09-30 às 16:20:23
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2345
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Bug, In progress, Mock Bank

**📝 Descrição:** #### 1. Observed Behavior: --- In the automatic payments flow in Mock Bank, when consent is not granted during redirection, a subsequent GET `/recurring-consents` request correctly updates the status ...

---

### 5. Issue #2344

**📌 Título:** Testes de timezone está chamando o endpoint incorreto - OCS-167

**👤 Autor:** Patrick Hadson (@pkhadson)
**📅 Criado:** 2025-09-30 às 01:52:24
**🔄 Atualizado:** 2025-09-30 às 19:46:08
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2344
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Bug, Conformance Suite
**📈 Estatísticas:** 💬 2 comentários

**📝 Descrição:** <!--Please note this form is only for reporting bugs/suggesting missing tests/etc. If you require support about certification policy or the API specifications please open a ticket on https://servicede...

---

### 6. Issue #2343

**📌 Título:** automatic-payments_api_automatic-pix-wrong-creditor_test-module_v2n2 - Incorrect polling behavior

**👤 Autor:** Bruno Pacheco (@bruno-augusto)
**📅 Criado:** 2025-09-29 às 22:20:25
**🔄 Atualizado:** 2025-09-30 às 12:44:38
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2343
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Conformance Suite, Under Evaluation

**📝 Descrição:** Test Case:  _(**automatic-payments_api_automatic-pix-wrong-creditor_test-module_v2n2)**_  Description:  According to the expected conformance behavior, once a transaction is created, the test suite sh...

---

### 7. Issue #2342

**📌 Título:** automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2 - Não considera inclusão do 'ibgeTownCode' da etapa de autorização

**👤 Autor:** Rafael de Freitas Cassalichio (@rafael.cassalichio)
**📅 Criado:** 2025-09-29 às 15:03:20
**🔄 Atualizado:** 2025-09-29 às 17:13:55
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2342
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Conformance Suite, Under Evaluation
**📈 Estatísticas:** 👍 3

**📝 Descrição:** Prezados, bom dia.  Durante execução do cenário "automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2" identificamos que a validação "EnsureOnlyCreditorNameFieldWasUpdated"...

---

### 8. Issue #2341

**📌 Título:** automatic-payments_api_automatic-pix_auxiliary-two-payments_test-module_v2n2 - Erro no segundo pagamento

**👤 Autor:** rodrigomagnos1 (@rodrigomagnos1)
**📅 Criado:** 2025-09-29 às 13:38:49
**🔄 Atualizado:** 2025-09-30 às 13:43:21
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2341
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Conformance Suite, Questions, Waiting Participant
**📈 Estatísticas:** 💬 1 comentários

**📝 Descrição:** Bom dia pessoal, tudo bem?  Temos uma dúvida em relação a criação de dois pagamento no auxiliary. Por questões de segurança, temos uma trava que impede a criação de um segundo pagamento com os mesmos ...

---

### 9. Issue #2337

**📌 Título:** Incluir retentativas nos testes FVP1.0

**👤 Autor:** Eri Silva (@eri.silva)
**📅 Criado:** 2025-09-26 às 14:46:24
**🔄 Atualizado:** 2025-09-30 às 12:49:26
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2337
**⚡ Estado:** OPENED
**🏷️ Labels:** FVP, Under WG/DTO Evaluation
**📈 Estatísticas:** 💬 1 comentários

**📝 Descrição:** Olá pessoal,  Nos últimos dias a FVP1.0, que faz testes diários, está experimentando 529 durante testes contra nossos servidores. Status 529 trata-se de quantidade de reqs por segundo (TPS) suportados...

---

### 10. Issue #2336

**📌 Título:** automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2 - riskSignals sent in patch

**👤 Autor:** João P Oliveira (@joao.oliveira24)
**📅 Criado:** 2025-09-26 às 14:29:25
**🔄 Atualizado:** 2025-09-30 às 20:20:21
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2336
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Conformance Suite, GT Serviços, Questions
**📈 Estatísticas:** 👍 2 | 💬 11 comentários

**📝 Descrição:** Why should not update riskSignals if they were sent?  In the docs says riskSignals is not mandatory for updating creditor name, but it is being sent by the conformance suite, and expecting it not to b...

---

### 11. Issue #2330

**📌 Título:** Update fvp-payments-consents-server-certificate-v2 to use POST instead of GET on payments/v4/consents - OCS-135

**👤 Autor:** Christian Eloysio (@christianraidiam)
**📅 Criado:** 2025-09-23 às 19:13:23
**🔄 Atualizado:** 2025-09-23 às 20:31:35
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2330
**⚡ Estado:** OPENED
**🏷️ Labels:** Backlog, Change Request, FVP, GT Serviços, Payments :: v4

**📝 Descrição:** **Observed Behavior:**\ The test module `fvp-payments-consents-server-certificate-v2` is performing a **GET** request on the `payments/v4/consents` endpoint. This endpoint only supports **POST**, so t...

---

### 12. Issue #2329

**📌 Título:** enrollments_api_automatic-payments_enrollment-limits_v2-2 – Divergence between firstPayment.amount in consent and the actual initial payment

**👤 Autor:** Carla Moreno (@carla-raidiam)
**📅 Criado:** 2025-09-23 às 18:05:43
**🔄 Atualizado:** 2025-09-30 às 12:48:11
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2329
**⚡ Estado:** OPENED
**🏷️ Labels:** Backlog, Change Request, No Redirect Payments :: v2, Squad JSR, Under WG/DTO Evaluation
**📈 Estatísticas:** 💬 4 comentários

**📝 Descrição:** #### 1. Observed Behavior: --- The test module `enrollments_api_automatic-payments_enrollment-limits_v2-2` currently defines that a POST `/recurring-consents` can be created when the `firstPayment.amo...

---

### 13. Issue #2326

**📌 Título:** automatic-payments_api_multiple-consents-core_test-module_v2n2 unexpected behavior - OCS-162

**👤 Autor:** Pio NEto (@PioNetoSisprime)
**📅 Criado:** 2025-09-22 às 20:16:40
**🔄 Atualizado:** 2025-09-30 às 12:46:41
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2326
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Backlog, Conformance Suite, GT Serviços, Test Improvement
**📈 Estatísticas:** 💬 1 comentários

**📝 Descrição:** **1) Expected Behavior** The mentioned test must stop after send a POST with an automatic payment and receive a 201 CREATED answers.  **2) Observed Behavior** As observed on the attatched logs, the te...

---

### 14. Issue #2325

**📌 Título:** fvp-payments_api_recurring-payments-monthly-core_open_test-module_v4 - OCS-159

**👤 Autor:** Matheus Rodrigues (@msfg01)
**📅 Criado:** 2025-09-22 às 14:11:15
**🔄 Atualizado:** 2025-09-29 às 14:11:08
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2325
**⚡ Estado:** OPENED
**🏷️ Labels:** Bug, FVP, GT Serviços, In progress, Payments :: v4
**📈 Estatísticas:** 💬 2 comentários

**📝 Descrição:** Good morning! We're running production FVP tests, and since Friday (September 19th) we've been receiving the following error: "Unable to find element resource.paymentAmount in config." We haven't made...

---

### 15. Issue #2315

**📌 Título:** automatic-payments_api_automatic-pix-extraday-retry-unaccepted_test-module_v2n2 - Motivo para 422 especificado no teste não é aceito pelo próprio teste

**👤 Autor:** Emerson Soares (@emerson.soares1)
**📅 Criado:** 2025-09-11 às 14:41:50
**🔄 Atualizado:** 2025-09-29 às 20:51:20
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2315
**⚡ Estado:** OPENED
**🏷️ Labels:** Automatic Payments::v2, Questions, Under WG/DTO Evaluation
**📈 Estatísticas:** 👍 1 | 💬 6 comentários

**📝 Descrição:** No roteiro do teste automatic-payments_api_automatic-pix-extraday-retry-unaccepted_test-module_v2n2, é esperado que o sistema retorne 422-PAGAMENTO_DIVERGENTE_CONSENTIMENTO para o envio de uma retenta...

---

### 16. Issue #2301

**📌 Título:** credit-portability_api_portability-patch-unhappy_test-module_v1 - Cancelamento realizado pela proponente. - OCI-4671

**👤 Autor:** Rafael de Freitas Cassalichio (@rafael.cassalichio)
**📅 Criado:** 2025-09-01 às 20:34:52
**🔄 Atualizado:** 2025-09-23 às 08:21:51
**🔗 URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2301
**⚡ Estado:** OPENED
**🏷️ Labels:** Change Request, Conformance Suite, Credit Portability::v1, GT Portabilidade de crédito, In progress
**📈 Estatísticas:** 👍 1 | 💬 3 comentários

**📝 Descrição:** Prezados, boa tarde.  O cenário "credit-portability_api_portability-patch-unhappy_test-module_v1", tenta realizar uma comunicação de cancelamento de uma portabilidade com status "ACCEPTED_SETTLEMENT_C...

---

