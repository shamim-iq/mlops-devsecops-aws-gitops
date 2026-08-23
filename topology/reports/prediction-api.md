# prediction-api Application Topology

Namespace: `prediction-api`

## Graph

```mermaid
flowchart LR
  ConfigMap_kube_root_ca_crt["ConfigMap: kube-root-ca.crt"]
  Pod_prediction_api_6cf6768455_4z8hb["Pod: prediction-api-6cf6768455-4z8hb"]
  ReplicaSet_prediction_api_57cdc9d9bd["ReplicaSet: prediction-api-57cdc9d9bd"]
  ReplicaSet_prediction_api_5d844cd8ff["ReplicaSet: prediction-api-5d844cd8ff"]
  ReplicaSet_prediction_api_6cf6768455["ReplicaSet: prediction-api-6cf6768455"]
  Rollout_prediction_api["Rollout: prediction-api"]
  Service_prediction_api["Service: prediction-api"]
  app["Application: prediction-api"]
  namespace["Namespace: prediction-api"]
  selector["Selector: app.kubernetes.io/name=prediction-api"]
  namespace -->|"contains"| app
  app -->|"selects"| selector
  selector -->|"matches"| Pod_prediction_api_6cf6768455_4z8hb
  Service_prediction_api -->|"selects"| Pod_prediction_api_6cf6768455_4z8hb
```

## Application

| name | namespace |
| --- | --- |
| prediction-api | prediction-api |

## ConfigMap

| name |
| --- |
| kube-root-ca.crt |

## Event

| message | object | reason |
| --- | --- | --- |
| Rollout updated to revision 10 | Rollout/prediction-api | RolloutUpdated |
| Rollback to stable ReplicaSets | Rollout/prediction-api | SkipSteps |

## Pod

| name |
| --- |
| prediction-api-6cf6768455-4z8hb |

## ReplicaSet

| name |
| --- |
| prediction-api-57cdc9d9bd |
| prediction-api-5d844cd8ff |
| prediction-api-6cf6768455 |

## Rollout

| name |
| --- |
| prediction-api |

## Selector

| labels |
| --- |
| app.kubernetes.io/name=prediction-api |

## Service

| name |
| --- |
| prediction-api |
