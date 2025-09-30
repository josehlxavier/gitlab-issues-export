# Issues do GitLab - Relatório Detalhado

**Data da extração:** 2025-09-30 18:06:44
**Total de issues:** 16

## Issue #2348: enrollments_automatic-payments_sweeping-consent-not-authorised_v2-2 – Non existent Error resons for 422 FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO

**Estado:** opened
**Autor:** Caio Tranjan (@caio.tranjan)
**Criado em:** 2025-09-30T18:24:46.018Z
**Atualizado em:** 2025-09-30T19:09:20.248Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2348
**Labels:** Automatic Payments::v2, Change Request, GT Serviços, Under WG/DTO Evaluation

### Descrição

Test Module was implemented following defined in: 'RAD-203'

Behavior:

enrollments_automatic-payments_sweeping-consent-not-authorised_v2-2

Test module summary:

<table>
<tr>
<th>

**Ensure a recurring consent for sweeping accounts cannot be successfully authorized.**

* **GET an SSA from the directory and ensure the field software_origin_uris, and extract the first uri from the array**
* **Execute a full enrollment journey sending the origin extracted above, extract the enrollment ID, and store the refresh_token generated ensuring it has the nrp-consents scope**
* **Call the GET enrollments endpoint**
* **Expect a 200 response - Validate the response and check if the status is "AUTHORISED"**
* **Call the POST recurring-consents endpoint with sweeping accounts data**
* **Expect 201 - Validate Response and ensure status as AWAITING_AUTHORISATION**
* **Call the GET recurring-consents endpoint**
* **Expect 200 - Validate Response and ensure status as AWAITING_AUTHORISATION**
* **Call the POST sign-options endpoint with the recurringConsentId created**
* **Expect 201 - Validate response and extract challenge**
* **Call the POST Token endpoint with the refresh_token grant, ensuring a token with the nrp-consent scope was issued**
* **Call POST recurring-consent authorize with valid payload, signing the challenge with the compliant private key**
* **Expects 422 with reason FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO**
* **Call GET recurring consent**
* **Expects 200 - Validate if status is "RJCT" and rejection.reason FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO**
</th>
</tr>
</table>

Steps with identified problem:

<table>
<tr>
<th>

* **Call POST recurring-consent authorize with valid payload, signing the challenge with the compliant private key**
* **Expects 422 with reason FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO**
</th>
</tr>
</table>

<table>
<tr>
<th>

* **Call GET recurring consent**
* **Expects 200 - Validate if status is "RJCT" and rejection.reason FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO**
</th>
</tr>
</table>

The mentioned reasons don't exist in the endpoints response;

* **POST recurring-consent authorize:**
  * Does not have: **422 with reason FLUXO_NAO_SUPORTADO_PRODUTO | PRODUTO_NAO_SUPORTADO**
* **GET recurring consent**
  * Does not have: **rejection.reason FLUXO_NAO_SUPORTADO_PRODUTO**

Suggestion:

* Removal the validation of this error and rejection reasons from the test module

What Needs evaluation from WG:

* Should we follow with the proposed suggestion?

---

## Issue #2347: PCM Failure on GET private/report - OCS-160

**Estado:** opened
**Autor:** Matheus Mantovani (@matheus-mantovani)
**Criado em:** 2025-09-30T17:30:09.860Z
**Atualizado em:** 2025-09-30T17:40:40.503Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2347
**Labels:** Backlog, Change Request, FVP

### Descrição

**Observed Behavior:**

PCM Fetch Logs endpoint

* GET `/report-api/v1/private/report/{fapiInteractionId}`

Fails to fetch reports, receiving error 401 from PCM.

Current FVP PCM integration was implemented following the specifications available at:

https://openfinancebrasil.atlassian.net/wiki/spaces/OF/pages/1062174721/Informa+es+T+cnicas+-+PCM+Telemetria+-+v2.1.2+Visualiza+o+Legada

![image.png](/uploads/5abcf5576f392c8732b26b9804417b19/image.png)

**Expected behavior:**

Although Not Specified in the Technical Documentation of PCM. During the Following endpoint Call:

* GET `/report-api/v1/private/report/{fapiInteractionId}` 

A PCM Access Token needs to be included as a Header on the GET Request.

---

## Issue #2346: Inconsistency in DCR generation – software_statement with invalid date

**Estado:** opened
**Autor:** Gutemberg Cedraz (@GutembergTeros)
**Criado em:** 2025-09-30T15:59:11.224Z
**Atualizado em:** 2025-09-30T16:48:08.512Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2346
**Labels:** FVP, Waiting Participant

### Descrição

During the registration/integration flow, the test engine issues the software_statement with an iat/date earlier than the current time, violating the requirement to issue with a valid, present timestamp, which invalidates the artifact at the registration endpoint.

![image.png](/uploads/82cb00ce9eaaafef2174d84eb01a26c6/image.png)

![image.png](/uploads/4a8de2a14e906ce222340afac5e837fa/image.png)

The component responsible for assembling the DCR is calculating the iat (issued at) based on an outdated clock or applying an incorrect time zone/epoch offset, resulting in a JWT with a timestamp prior to the validation moment.

Plan ID: lJi4JUDSwbkYe

Test ID: QxbfAyWHlcPZdAU

---

## Issue #2345: Rejected consent at redirection missing rejection object

**Estado:** opened
**Autor:** Carla Moreno (@carla-raidiam)
**Criado em:** 2025-09-30T13:05:42.603Z
**Atualizado em:** 2025-09-30T16:20:23.148Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2345
**Labels:** Automatic Payments::v2, Bug, In progress, Mock Bank

### Descrição

#### 1. Observed Behavior:
---
In the automatic payments flow in Mock Bank, when consent is not granted during redirection, a subsequent GET `/recurring-consents` request correctly updates the status to `REJECTED`, but the `rejection` object is not returned.

#### 2. Expected Behavior:
---
According to the specification ([API Automatic Payments v2.2.0-rc.2](https://raw.githubusercontent.com/OpenBanking-Brasil/all-services-repo/refs/heads/main/api_automatic_payments_-_open_finance_brasil/2.2.0-rc.2.yaml)), the object rejection is mandatory when the status is REJECTED:

![image](/uploads/f8a8d3f57f2c73d416e532df16581069/image.png)

#### 3. Evidence:
---

- `x-fapi-interaction-id`: `c504d374-8676-4481-be13-a1f030c971d2`
- Date of the test: 18/09/2025
- Full GET response:

```
21:06:12.199 [io-executor-thread-23] INFO  c.r.t.bank.utils.BankLambdaUtils - ResponseRecurringConsentV2 - 
{
    "data": {
        "recurringConsentId": "urn:raidiambank:42b39bc2-d263-4565-80cf-d3a8259554aa",
        "statusUpdateDateTime": "2025-09-18T21:05:53Z",
        "loggedUser": {
            "document": {
                "identification": "76109277673",
                "rel": "CPF"
            }
        },
        "businessEntity": {
            "document": {
                "identification": "11111111111111",
                "rel": "CNPJ"
            }
        },
        "status": "REJECTED",
        "creditors": [
            {
                "personType": "PESSOA_JURIDICA",
                "cpfCnpj": "11111111111111",
                "name": "Empresa X"
            }
        ],
        "creationDateTime": "2025-09-18T21:05:14Z",
        "expirationDateTime": "2025-09-30T23:59:59Z",
        "recurringConfiguration": {
            "automatic": {
                "contractId": "hcGG31HvR3SqOlHva6XKk",
                "minimumVariableAmount": "20.00",
                "maximumVariableAmount": "200.00",
                "interval": "SEMANAL",
                "contractDebtor": {
                    "name": "Marco Antonio de Brito",
                    "document": {
                        "identification": "76109277673",
                        "rel": "CPF"
                    }
                },
                "firstPayment": {
                    "type": "PIX",
                    "date": "2025-09-29",
                    "currency": "BRL",
                    "amount": "20.50",
                    "creditorAccount": {
                        "ispb": "12345678",
                        "issuer": "4000",
                        "number": "200",
                        "accountType": "SVGS"
                    }
                },
                "isRetryAccepted": true,
                "useOverdraftLimit": false,
                "referenceStartDate": "2025-09-30"
            }
        }
    },
    "links": {
        "self": "https://matls-api.mockbank.poc.raidiam.io/open-banking/automatic-payments/v2/recurring-consents/urn:raidiambank:42b39bc2-d263-4565-80cf-d3a8259554aa"
    },
    "meta": {
        "requestDateTime": "2025-09-18T21:06:12Z"
    }
}
```

---

## Issue #2344: Testes de timezone está chamando o endpoint incorreto - OCS-167

**Estado:** opened
**Autor:** Patrick Hadson (@pkhadson)
**Criado em:** 2025-09-30T01:52:24.118Z
**Atualizado em:** 2025-09-30T19:46:08.629Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2344
**Labels:** Automatic Payments::v2, Bug, Conformance Suite

### Descrição

<!--Please note this form is only for reporting bugs/suggesting missing tests/etc. If you require support about certification policy or the API specifications please open a ticket on https://servicedesk.openfinancebrasil.org.br/

*If you believe a failure the conformance suite is reporting is not a valid failure, you MUST include a hyperlink for the exact section of the relevant specification that explains how the behavior of your software is compliant, and you MUST include a quote of the exact clause/phrase you are relying on*

*If the problem relates to a test, please provide a link to the log-detail.html page on our server (the test result does NOT need to be 'published')*-->

#### Current Behavior:

---

Describe the behavior you are currently experiencing. What is happening that you believe is incorrect or unexpected?

Ao rodar os testes de timezone, no roteiro do teste menciona uma chamada no `GET recurring-payments/{recurringPaymentId}`. Mas essa chamada nunca acontece, a chamada que está sendo feita é a `GET recurring-payments?recurringConsentId={recurringConsentId}`.

`GET recurring-payments/{recurringPaymentId}` retorna `data` como um objeto, e `GET recurring-payments?recurringConsentId={recurringConsentId}` retorna `data` como um array. O teste está quebrando por esperar um objeto e receber um array.

#### Expected Behavior:

---

Explain the behavior you were expecting to see instead. How do you think the system should behave?

O teste deveria fazer a chamada para o `GET recurring-payments/{recurringPaymentId}`.

#### Evidence:

---

Provide any relevant evidence such as screenshots, logs, or data tables that support your report.

| Test Name | Test ID | Plan ID | URL |
|-----------|---------|---------|-----|
| automatic-payments_api_automatic-pix-receiver-revoked-consent-timezone_test-module_v2-2 | gxLRU8ED9jFy2rx | ZB4Gt0h8YuMgE | https://web.conformance.directory.openbankingbrasil.org.br/log-detail.html?log=gxLRU8ED9jFy2rx&public=true |
| automatic-payments_api_automatic-pix-user-revoked-consent-timezone_test-module_v2-2 | 9X7slCfddFXbeN8 | 0crKnJvNxJa89 | https://web.conformance.directory.openbankingbrasil.org.br/log-detail.html?log=9X7slCfddFXbeN8&public=true |

---

Update:

**This issue is the reference for 2331, 2339, and 2340, as they all will be covered by the same action in OCS-167, related to following tests:**

* automatic-payments_api_automatic-pix-receiver-revoked-consent-timezone_test-module_v2-2
* automatic-payments_api_automatic-pix-user-revoked-consent-timezone_test-module_v2-2

---

## Issue #2343: automatic-payments_api_automatic-pix-wrong-creditor_test-module_v2n2 - Incorrect polling behavior

**Estado:** opened
**Autor:** Bruno Pacheco (@bruno-augusto)
**Criado em:** 2025-09-29T22:20:25.059Z
**Atualizado em:** 2025-09-30T12:44:38.825Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2343
**Labels:** Automatic Payments::v2, Conformance Suite, Under Evaluation

### Descrição

Test Case:  _(**automatic-payments_api_automatic-pix-wrong-creditor_test-module_v2n2)**_

Description:

According to the expected conformance behavior, once a transaction is created, the test suite should repeatedly pool the participant's _/**v2/pix/recurring-payments/**_  endpoint until the transaction reaches a final status (e.g., RJCT, CANC, etc.), or until a defined timeout condition is met.

Currently, the polling mechanism appears to be executed only a single time. If the initial response does not already contain a final status, the test fails immediately rather than continuing the polling cycle.

Expected behavior:

* After a transaction is created, the test suite should keep polling the _/**v2/pix/recurring-payments/**_ endpoint at regular intervals.
* Polling should continue until one of the following conditions is satisfied:
  * The transaction reaches a final status as defined in the standard (e.g., RJCT).
  * The maximum allowed polling duration (timeout) is exceeded.

Actual behavior:

* Only one polling request is issued after transaction creation.
* If the transaction is still in a transitional state, the test case fails prematurely.

Impact: This behavior prevents proper validation of the transaction lifecycle. Since transitional states are part of the normal flow before reaching a final outcome, the absence of iterative polling may lead to false negatives during conformance testing.

Evidence:

1. Polling being executed only once

![polling-sequence-once.png](/uploads/252accee1c9db80bffef0c714844d69b/polling-sequence-once.png){width=1440 height=703}

2. Test case failing in the first polling request

![rejection-raidiam.png](/uploads/bc27e32724bccd3dab7639c54c235158/rejection-raidiam.png){width=1032 height=502}

3. Plan & Test infos:

   | **Test ID** | Onmd50AkmDiqw6r https://web.conformance.directory.openbankingbrasil.org.br/log-detail.html?public=true&log=Onmd50AkmDiqw6r |
   |-------------|----------------------------------------------------------------------------------------------------------------------------|
   | **Plan ID** | z09MTyMa1ti1O https://web.conformance.directory.openbankingbrasil.org.br/plan-detail.html?public=true&plan=z09MTyMa1ti1O |


Additional Validation:

We have validated internally that the issue is not related to out GET endpoint implementation.

During our internal testing, we observed that if at least one additional polling attempt had been performed, the transaction would have been correctly returned with its final rejection status (RJCT).

---

## Issue #2342: automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2 - Não considera inclusão do 'ibgeTownCode' da etapa de autorização

**Estado:** opened
**Autor:** Rafael de Freitas Cassalichio (@rafael.cassalichio)
**Criado em:** 2025-09-29T15:03:20.765Z
**Atualizado em:** 2025-09-29T17:13:55.351Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2342
**Labels:** Automatic Payments::v2, Conformance Suite, Under Evaluation

### Descrição

Prezados, bom dia.

Durante execução do cenário "automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2" identificamos que a validação "EnsureOnlyCreditorNameFieldWasUpdated" está comparando um corpo de resposta pré autorização, com um corpo de resposta pós autorização e edição, e esperando que esteja alterado apenas o creditors.name (parâmetro editado), sem levar em consideração que o atributo ibgeTownCode, é adicionado ao consentimento antes/durante a autorização. 

![image](/uploads/e7698f9a8905276979636492b6e27621/image.png){width=1230 height=582}

![image](/uploads/fe034cd62db275955e875329a170722d/image.png){width=556 height=132}

Além disso, o corpo de resposta considerado "current" nessa validação, não contém o 'creditors.name' "Openflix", mesmo ele estando presente em todas as consultas pós edição. 

![image](/uploads/c5cb84a91f8720eeab3fb16716639d62/image.png){width=906 height=503}
![image](/uploads/883de847cc696dc5a39b2453e25d7076/image.png){width=531 height=538}

Poderiam verificar? Trata-se de um dos cenários obrigatórios para o marco de 100%.

| Test Name | Test ID | Plan ID |
|-----------|---------|---------|
| automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2 | 7hdJ8S6mA9jX2D8 | aq1jvGjE3EsCq |

---

## Issue #2341: automatic-payments_api_automatic-pix_auxiliary-two-payments_test-module_v2n2 - Erro no segundo pagamento

**Estado:** opened
**Autor:** rodrigomagnos1 (@rodrigomagnos1)
**Criado em:** 2025-09-29T13:38:49.400Z
**Atualizado em:** 2025-09-30T13:43:21.610Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2341
**Labels:** Automatic Payments::v2, Conformance Suite, Questions, Waiting Participant

### Descrição

Bom dia pessoal, tudo bem?

Temos uma dúvida em relação a criação de dois pagamento no auxiliary. Por questões de segurança, temos uma trava que impede a criação de um segundo pagamento com os mesmos dados do pagador, data de vencimento e valor em um intervalo menor que 3 minutos, ou seja, a partir do momento em que for enviado o primeiro pagamento, somente após 3 min seria possível mandar o segundo (com o mesmo valor, dados do pagador e data de vencimento). Minha dúvida é se é possível enviar o segundo pagamento com um valor diferente do primeiro.

---

## Issue #2337: Incluir retentativas nos testes FVP1.0

**Estado:** opened
**Autor:** Eri Silva (@eri.silva)
**Criado em:** 2025-09-26T14:46:24.019Z
**Atualizado em:** 2025-09-30T12:49:26.332Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2337
**Labels:** FVP, Under WG/DTO Evaluation

### Descrição

Olá pessoal,

Nos últimos dias a FVP1.0, que faz testes diários, está experimentando 529 durante testes contra nossos servidores.
Status 529 trata-se de quantidade de reqs por segundo (TPS) suportados pela infraestrutura SERVER, e deve ser ajustado a cada 45 dias, se necessário.
- Fonte: https://openfinancebrasil.atlassian.net/wiki/spaces/OF/pages/17989722/Limites+de+tr+fego#Limites-globais---TPS-(Transa%C3%A7%C3%B5es-por-segundo)

Considerando isto, podem ajustar os testes da FVP1.0 para, em casos de 529, executar 3 a 5 retentativas ao longo de minutos simulando um pouco de recomendações de polling que as Receptoras do ecossistema atualmente seguem? Esse ajuste soa adequado para os propósitos da FVP1.0, e padrões de funcionamento do ambiente produtivo. Isso mantém a ferramenta executando 1 teste diário, mas cada passo do teste retentar acessar o mesmo endpoint em casos de 529.
- Uma possibilidade, ainda, seria reexecutar o mesmo teste em momentos diferentes do dia, o que é possivelmente mais simples, pois não necessitaria de ajustes nas atuais definições do teste, apenas nos jobs de execuções.

Agradecemos desde já pela consideração.

---

## Issue #2336: automatic-payments_api_automatic-pix-consent-edition-permissive_test-module_v2n2 - riskSignals sent in patch

**Estado:** opened
**Autor:** João P Oliveira (@joao.oliveira24)
**Criado em:** 2025-09-26T14:29:25.507Z
**Atualizado em:** 2025-09-30T20:20:21.072Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2336
**Labels:** Automatic Payments::v2, Conformance Suite, GT Serviços, Questions

### Descrição


Why should not update riskSignals if they were sent? 
In the docs says riskSignals is not mandatory for updating creditor name, but it is being sent by the conformance suite, and expecting it not to be updated, is this  behavior correct?

```
{
  "iss": "0add85e7-086c-41d0-bd35-a3641d7acc36",
  "aud": "https://mtls.lina.hml.linaob.com.br/open-banking/automatic-payments/v2/recurring-consents/urn:lina:fbe0f0fe-8673-4166-bad8-69a00b79a39d",
  "data": {
    "creditors": [
      {
        "name": "Openflix"
      }
    ],
    "loggedUser": {
      "document": {
        "identification": "01234567890",
        "rel": "CPF"
      }
    },
    "riskSignals": {
      "deviceId": "00000000-54b3-e7c7-0000-000046bffd97",
      "isRootedDevice": false,
      "screenBrightness": 0,
      "elapsedTimeSinceBoot": 0,
      "osVersion": "string",
      "userTimeZoneOffset": "string",
      "language": "string",
      "accountTenure": "2024-12-17",
      "screenDimensions": {
        "width": 0,
        "height": 0
      }
    }
  },
  "iat": 1758895575,
  "jti": "65196b53-0dff-4f18-8234-476c50901fec"
}
```

![image](/uploads/e729715f00baec0aa1c6c1ed24c2f6ce/image.png){width=843 height=225}

---

## Issue #2330: Update fvp-payments-consents-server-certificate-v2 to use POST instead of GET on payments/v4/consents - OCS-135

**Estado:** opened
**Autor:** Christian Eloysio (@christianraidiam)
**Criado em:** 2025-09-23T19:13:23.614Z
**Atualizado em:** 2025-09-23T20:31:35.015Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2330
**Labels:** Backlog, Change Request, FVP, GT Serviços, Payments :: v4

### Descrição

**Observed Behavior:**\
The test module `fvp-payments-consents-server-certificate-v2` is performing a **GET** request on the `payments/v4/consents` endpoint. This endpoint only supports **POST**, so the request fails. Although the test logic for certificate validation is technically correct, this behavior breaks PCM integration and causes inconsistencies in platform interoperability.

**Expected Behavior:**

* The test should use **POST** instead of GET when calling the `payments/v4/consents` endpoint.
* Continue validating the server certificate chain according to RFC5246 - 7.4.2.
* Ensure compatibility with PCM and other dependent integrations by using the correct HTTP method.

**Tracking:** This issue is being tracked in the Open Finance task board under **RAD-247**:\
https://openfinancebrasil.atlassian.net/browse/RAD-247

---

## Issue #2329: enrollments_api_automatic-payments_enrollment-limits_v2-2 – Divergence between firstPayment.amount in consent and the actual initial payment

**Estado:** opened
**Autor:** Carla Moreno (@carla-raidiam)
**Criado em:** 2025-09-23T18:05:43.543Z
**Atualizado em:** 2025-09-30T12:48:11.932Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2329
**Labels:** Backlog, Change Request, No Redirect Payments :: v2, Squad JSR, Under WG/DTO Evaluation

### Descrição

#### 1. Observed Behavior:
---
The test module `enrollments_api_automatic-payments_enrollment-limits_v2-2` currently defines that a POST `/recurring-consents` can be created when the `firstPayment.amount` exceeds the `transactionLimit` of the enrollment. However, the test then proceeds with a POST `/recurring-payments` for the initial payment using a different amount than the one defined in the consent and expects success, which does not seem correct.

This raises the question of whether this behaviour should indeed be expected, as it appears inconsistent with the principle that payments must respect the consented amount. If not correct, clarification is needed on what should be the update in the test.

It follows test behaviour and relevant test steps are highlighted in **bold** below:

> Ensure that an Automatic Pix recurring payment can be executed if it is above the enrollment limits, provided it respects consent limits <br>
• GET an SSA from the directory and ensure the field software_origin_uris, and extract the first uri from the array <br>
• Execute a full enrollment journey sending the origin extracted above, extract the enrollment ID, and store the refresh_token generated ensuring it has the nrp-consents scope <br>
• Call the GET /enrollments/{enrollment_id} endpoint <br>
• Expect a 200 response - Validate the response and check if the status is "AUTHORISED", and **retrieve transactionLimit** <br>
• Call the POST /recurring-consents endpoint sending product as "AUTOMATIC_PIX", referenceStartDate as D+1, interval as "SEMANAL", automatic.fixedAmount **and firstPayment.amount as enrollment transactionLimit + 1.00 BRL**, firstPayment.date as D+0 <br>
• Expects a 201 response <br>
• Call the POST /sign-options <br>
• Expect a 201 response <br>
• Call the POST /recurring-consents/authorise <br>
• Expect a 204 response <br>
• **Call the POST /recurring-payments endpoint sending payment.amount as enrollment transactionLimit**, date as D+0 <br>
• **Expect a 201 response - Validate response** <br>
• Poll the GET /recurring-payments/{recurringPaymentId} endpoint while status is "RCVD", "ACCP" or "ACPD" <br>
• Call the GET /recurring-payments/{recurringPaymentId} endpoint <br>
• Expect a 200 response - Validate response: status as "ACSC" <br>
• Call the POST /recurring-payments endpoint sending payment.amount as enrollment transactionLimit + 1.00 BRL, date as D+2 <br>
• Expect a 201 response <br>
• Poll the GET /recurring-payments/{recurringPaymentId} endpoint while status is "RCVD", "ACCP" or "ACPD" <br>
• Call the GET /recurring-payments/{recurringPaymentId} endpoint <br>
• Expect a 200 response - Validate status as "SCHD" <br>
>

#### 2. Expected Behavior:
---
We need confirmation whether this current behaviour is correct, because while the consent, indeed, must be able to be created and authorised even if the `firstPayment.amount` exceeds the enrollment `transactionLimit`, as proposed, we believe the first payment should strictly follow the `firstPayment.amount` defined in the consent. If the payment amount differs from the consent, an error should be expected (422 `PAGAMENTO_DIVERGENTE_CONSENTIMENTO`). 

The current behaviour in the test module does not appear consistent with this expectation. Could DTO/WG clarify whether this behaviour is correct or if the test should instead expect an error, please?

---

## Issue #2326: automatic-payments_api_multiple-consents-core_test-module_v2n2 unexpected behavior - OCS-162

**Estado:** opened
**Autor:** Pio NEto (@PioNetoSisprime)
**Criado em:** 2025-09-22T20:16:40.110Z
**Atualizado em:** 2025-09-30T12:46:41.994Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2326
**Labels:** Automatic Payments::v2, Backlog, Conformance Suite, GT Serviços, Test Improvement

### Descrição

**1) Expected Behavior**
The mentioned test must stop after send a POST with an automatic payment and receive a 201 CREATED answers.

**2) Observed Behavior**
As observed on the attatched logs, the test starts pooling GET requests to validate some status, but the test doesn't mention what will be validated.
[test-log-automatic-payments_api_multiple-consents-core_test-module_v2n2-private_key_jwt-pushed-openbanking_brazil-plain_response-xldnBm6P0vGtnGR.zip](/uploads/aec5377aeeea1b144ab9fcb849f6299c/test-log-automatic-payments_api_multiple-consents-core_test-module_v2n2-private_key_jwt-pushed-openbanking_brazil-plain_response-xldnBm6P0vGtnGR.zip)

---

## Issue #2325: fvp-payments_api_recurring-payments-monthly-core_open_test-module_v4 - OCS-159

**Estado:** opened
**Autor:** Matheus Rodrigues (@msfg01)
**Criado em:** 2025-09-22T14:11:15.441Z
**Atualizado em:** 2025-09-29T14:11:08.569Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2325
**Labels:** Bug, FVP, GT Serviços, In progress, Payments :: v4

### Descrição

Good morning! We're running production FVP tests, and since Friday (September 19th) we've been receiving the following error: "Unable to find element resource.paymentAmount in config." We haven't made any configuration changes. Can you help us? Thank you!

![image](/uploads/393923ef2e8816cf73008c96389e72bf/image.png){width=858 height=160}

![image](/uploads/f5e3c6c59855a3b0c1ea27a8d327727d/image.png){width=1318 height=447}

---

## Issue #2315: automatic-payments_api_automatic-pix-extraday-retry-unaccepted_test-module_v2n2 - Motivo para 422 especificado no teste não é aceito pelo próprio teste

**Estado:** opened
**Autor:** Emerson Soares (@emerson.soares1)
**Criado em:** 2025-09-11T14:41:50.546Z
**Atualizado em:** 2025-09-29T20:51:20.962Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2315
**Labels:** Automatic Payments::v2, Questions, Under WG/DTO Evaluation

### Descrição

No roteiro do teste automatic-payments_api_automatic-pix-extraday-retry-unaccepted_test-module_v2n2, é esperado que o sistema retorne 422-PAGAMENTO_DIVERGENTE_CONSENTIMENTO para o envio de uma retentativa de um pagamento quando o consentimento está configurado para não aceitar consentimento.

No entanto, ao retornar o valor esperado, o motor de testes acusa falha pois este valor (PAGAMENTO_DIVERGENTE_CONSENTIMENTO) não é especificado na documentação do novo endpoint de retentativa.

---

## Issue #2301: credit-portability_api_portability-patch-unhappy_test-module_v1 - Cancelamento realizado pela proponente. - OCI-4671

**Estado:** opened
**Autor:** Rafael de Freitas Cassalichio (@rafael.cassalichio)
**Criado em:** 2025-09-01T20:34:52.795Z
**Atualizado em:** 2025-09-23T08:21:51.670Z
**URL:** https://gitlab.com/raidiam-conformance/open-finance/certification/-/issues/2301
**Labels:** Change Request, Conformance Suite, Credit Portability::v1, GT Portabilidade de crédito, In progress

### Descrição

Prezados, boa tarde.

O cenário "credit-portability_api_portability-patch-unhappy_test-module_v1", tenta realizar uma comunicação de cancelamento de uma portabilidade com status "ACCEPTED_SETTLEMENT_COMPLETED" e espera receber um retorno 422, uma vez que a portabilidade não poderia ser cancelada pelo cliente neste status.

Porém, o teste está informando o 'reason.type' como "CANCELADO_PELO_CLIENTE" e o 'rejectedBy' como "PROPONENTE", conforme evidência:

![image](/uploads/10d76d63cd68966c613b052285eb7d47/image.png){width=519 height=342}

Apesar do reason.type informado, o rejectedBy é "PROPONENTE" e segundo a máquina de estados, essa portabilidade pode ser rejeitada pela proponente:

![image](/uploads/f4029a62a91f7ecaeb7ad3f73b776f48/image.png){width=951 height=507}

O que faz o cenário não se comportar conforme esperado.

Além disso, na issue #2239 chegamos ao entendimento que o 'reason.type' "CANCELADO_PELO_CLIENTE" nunca deveria ser atrelado a um 'rejectedBy' "PROPONENTE", já que o 'rejectedBy' indica quem realizou a rejeição e não quem está comunicando ela:

![image](/uploads/01eff3030ee0f9e4c4ecb077f7a46143/image.png){width=901 height=288}

Poderiam verificar esse cenário?


| Test Name | Test ID | Plan ID |
| --------- | ------- | ------- |
| credit-portability_api_portability-patch-unhappy_test-module_v1 | OfbqdTUlydkuGwr | 8J1Hg3CuE0wLE |

---

