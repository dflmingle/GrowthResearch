# 一手来源与证据目录

本轮是公开技术研究和自主架构设计，不是厂商生产逆向复原。未安装/运行解析库、SDK、服务或模型；未访问身份接口、投放端点、真实个人记录；76号程序不改、不重跑。**C_graph.Axon=UNKNOWN；C_graph.Vector=UNKNOWN；D=UNKNOWN；原生产取证STOP。** 第三方开源能力、协议和论文都不归属于Axon或Vector。

证据类别分REF_DOC（作者/项目文档）、REF_CODE（限定函数静态代码）、PROTOCOL（协议规范）、PAPER（原始论文重点段落）、VENDOR_CONTRACT（既有合作方契约）和DESIGN（本地拟议）。这些类别不是厂商生产E5/E6升级。源码commit、声明版本、采集时间、发布时间分开。

## 新增原文摘录


### SIR01 · Fellegi–Sunter模型以m/u及先验刻画证据；不是设备图谱产品

来源：https://raw.githubusercontent.com/moj-analytical-services/splink/f319070e56c5b3666ec512811ac1820070f6f2e5/docs/topic_guides/theory/fellegi_sunter.md；采集：2026-11-20T08:36:07.873056+00:00；REF_DOC；范围：Splink pinned documentation。

原件：`server-identity-reference/sources/splink-theory.raw`；SHA256 `d0a1d728d00a051881f66636a3f040db258cbb6d6d28171302e2c8aa0d08b88a`。正文：`server-identity-reference/sources/splink-theory.raw` L13–20，SHA256 `d0a1d728d00a051881f66636a3f040db258cbb6d6d28171302e2c8aa0d08b88a`。许可/用途：MIT。

```text
!!! note ""
    * $\lambda$ - probability that any two records match
    * $m$ - probability of a given observation *given* the records are a match
    * $u$ - probability of a given observation *given* the records are **not** a match

<hr>

### λ probability
```


### SIR02 · 条件独立假设影响组合分数，不能当无条件校准置信度

来源：https://raw.githubusercontent.com/moj-analytical-services/splink/f319070e56c5b3666ec512811ac1820070f6f2e5/docs/topic_guides/theory/fellegi_sunter.md；采集：2026-11-20T08:36:07.873056+00:00；REF_DOC；范围：Splink theory, selected paragraph。

原件：`server-identity-reference/sources/splink-theory.raw`；SHA256 `d0a1d728d00a051881f66636a3f040db258cbb6d6d28171302e2c8aa0d08b88a`。正文：`server-identity-reference/sources/splink-theory.raw` L127–135，SHA256 `d0a1d728d00a051881f66636a3f040db258cbb6d6d28171302e2c8aa0d08b88a`。许可/用途：MIT。

```text
where $\lambda$ is the probability that two random records match and $K=m/u$ is the Bayes factor.

A key assumption of the Fellegi Sunter model is that observations from different column/comparisons are independent of one another. This means that the Bayes factor for two records is the products of the Bayes factor for each column/comparison:

$$ K_\textsf{features} = K_\textsf{forename} \cdot K_\textsf{surname} \cdot K_\textsf{dob} \cdot K_\textsf{city} \cdot K_\textsf{email} $$

This, in turn, means that match weights are additive:

$$ M_\textsf{obs} = M_\textsf{prior} + M_\textsf{features} $$
```


### SIR03 · 阈值决定误合并/漏合并取舍

来源：https://raw.githubusercontent.com/moj-analytical-services/splink/f319070e56c5b3666ec512811ac1820070f6f2e5/docs/topic_guides/theory/probabilistic_vs_deterministic.md；采集：2026-11-20T08:36:07.874056+00:00；REF_DOC；范围：Record linkage routes; not authenticated-login proof。

原件：`server-identity-reference/sources/splink-deterministic.raw`；SHA256 `49f5e10c6d3c5a3cca9f277bf836bc69f15d7cf99dc7733c933de3096d6433d2`。正文：`server-identity-reference/sources/splink-deterministic.raw` L76–83，SHA256 `49f5e10c6d3c5a3cca9f277bf836bc69f15d7cf99dc7733c933de3096d6433d2`。许可/用途：MIT。

```text
This is important, as it allows the linkage to be customised to best support the specific use case. For example, if it is important to:

* minimise False Positive matches (i.e. where False Negatives are less of a concern), a higher threshold for a match can be chosen.
* maximise True Positive matches (i.e. where False Positives are less of a concern), a lower threshold can be chosen.

!!! info "Further Reading"
    For a more in-depth introduction to Probabilistic Data Linkage, including an interactive version of the waterfall chart above, see [Robin Linacre's Blog](https://www.robinlinacre.com/intro_to_probabilistic_linkage/).

```


### SIR04 · 阈值后连通分量聚类是实现选择，不等于所有对都已独立确认

来源：https://raw.githubusercontent.com/moj-analytical-services/splink/f319070e56c5b3666ec512811ac1820070f6f2e5/splink/internals/clustering.py；采集：2026-11-20T08:36:07.875056+00:00；REF_CODE；范围：Only selected function/docstring, not full package behavior。

原件：`server-identity-reference/sources/splink-cluster-code.raw`；SHA256 `2d5127753ff54f32387c437075211c8497fd43b006fbd898bd2d488b932c9367`。正文：`server-identity-reference/sources/splink-cluster-code.raw` L42–69，SHA256 `2d5127753ff54f32387c437075211c8497fd43b006fbd898bd2d488b932c9367`。许可/用途：MIT。

```text


def cluster_pairwise_predictions_at_threshold(
    nodes: AcceptableInputTableType,
    edges: AcceptableInputTableType,
    db_api: DatabaseAPISubClass,
    node_id_column_name: str,
    edge_id_column_name_left: Optional[str] = None,
    edge_id_column_name_right: Optional[str] = None,
    threshold_match_probability: Optional[float] = None,
    threshold_match_weight: Optional[float] = None,
) -> SplinkDataFrame:
    """Clusters the pairwise match predictions into groups of connected records using
    the connected components graph clustering algorithm.

    Records with an estimated match probability at or above threshold_match_probability
    are considered to be a match (i.e. they represent the same entity).

    If no match probability or match weight is provided, it is assumed that all edges
    (comparison) are a match.

    If your node and edge column names follow Splink naming conventions, then you can
    omit edge_id_column_name_left and edge_id_column_name_right. For example, if you
    have a table of nodes with a column `unique_id`, it would be assumed that the
    edge table has columns `unique_id_l` and `unique_id_r`.

    Args:
        nodes (AcceptableInputTableType): The table containing node information
```


### SIR05 · 文档描述字段距离、正则逻辑回归及标注训练

来源：https://raw.githubusercontent.com/dedupeio/dedupe/3f61e79102910bd355e920a2df7e44c14c9cb247/docs/how-it-works/Matching-records.rst；采集：2026-11-20T08:36:08.990534+00:00；REF_DOC；范围：dedupe algorithm description, not current dependency-runtime verification。

原件：`server-identity-reference/sources/dedupe-matching.raw`；SHA256 `4a94b896532a1128ba1264a90db2da1a2f84392947aced25afa793d6ba07e841`。正文：`server-identity-reference/sources/dedupe-matching.raw` L91–100，SHA256 `4a94b896532a1128ba1264a90db2da1a2f84392947aced25afa793d6ba07e841`。许可/用途：MIT。

```text

Fortunately, we can solve both problems with a technique called
regularized logistic regression. If we supply pairs of records that we
label as either being duplicates or distinct, then Dedupe will learn a
set of weights such that the record distance can easily be transformed
into our best estimate of the probability that a pair of records are
duplicates.

Once we have learned these good weights, we want to use them to find
which records are duplicates. But turns out that doing this the naive
```


### SIR06 · 主动学习样本不代表部署分布，阈值/校准须另验证

来源：https://raw.githubusercontent.com/dedupeio/dedupe/3f61e79102910bd355e920a2df7e44c14c9cb247/docs/how-it-works/Choosing-a-good-threshold.rst；采集：2026-11-20T08:36:08.991534+00:00；REF_DOC；范围：dedupe threshold documentation。

原件：`server-identity-reference/sources/dedupe-threshold.raw`；SHA256 `90a037b45d8543a72411e804e9cc357b8e0649c586bee9f2d0a8c52f4feb9042`。正文：`server-identity-reference/sources/dedupe-threshold.raw` L25–33，SHA256 `90a037b45d8543a72411e804e9cc357b8e0649c586bee9f2d0a8c52f4feb9042`。许可/用途：MIT。

```text

So here's the problem - the labeled examples that we make with Dedupe
are not at all representative, and that's by design. In the active
learning step, we are not trying to find the most representative data
examples. We're trying to find the ones that will teach us the most.

The approach we take here is to take a random sample of blocked data,
and then calculate the pairwise probability that records will be
duplicates within each block. From these probabilities we can calculate
```


### SIR07 · 所选代码调用centroid linkage和fcluster

来源：https://raw.githubusercontent.com/dedupeio/dedupe/3f61e79102910bd355e920a2df7e44c14c9cb247/dedupe/clustering.py；采集：2026-11-20T08:36:09.600036+00:00；REF_CODE；范围：dedupe cluster function snippet only。

原件：`server-identity-reference/sources/dedupe-cluster-code.raw`；SHA256 `4ce419422aa800dde48b213369d34dd5801b7736773b5bffe45464896b9e0f6d`。正文：`server-identity-reference/sources/dedupe-cluster-code.raw` L232–242，SHA256 `4ce419422aa800dde48b213369d34dd5801b7736773b5bffe45464896b9e0f6d`。许可/用途：MIT。

```text

            linkage = scipy.cluster.hierarchy.linkage(
                condensed_distances, method="centroid"
            )

            partition = scipy.cluster.hierarchy.fcluster(
                linkage, distance_threshold, criterion="distance"
            )

            clusters: dict[int, list[int]] = defaultdict(list)

```


### SIR08 · 两两估计概率不具传递性；文档不是普遍数学最优结论

来源：https://raw.githubusercontent.com/dedupeio/dedupe/3f61e79102910bd355e920a2df7e44c14c9cb247/docs/how-it-works/Grouping-duplicates.rst；采集：2026-11-20T08:36:08.990534+00:00；REF_DOC；范围：dedupe clustering rationale。

原件：`server-identity-reference/sources/dedupe-grouping.raw`；SHA256 `515ba2aa2fde6e04c87fe8ebeab7ac6b422fecd8036397ed7eb2e8a6b5e855ee`。正文：`server-identity-reference/sources/dedupe-grouping.raw` L36–45，SHA256 `515ba2aa2fde6e04c87fe8ebeab7ac6b422fecd8036397ed7eb2e8a6b5e855ee`。许可/用途：MIT。

```text

Unfortunately, a more principled answer does not exist because the
estimated pairwise probabilities are not transitive.

Clustering the groups depends on us setting a threshold for group
membership -- the distance of the points to the centroid. Depending on how
we choose that threshold, we'll get very different groups, and we will
want to choose this threshold wisely.

In recent years, there has been some very exciting research that
```


### SIR09 · 分类支持match/nonmatch/possible match及监督/非监督路线

来源：https://raw.githubusercontent.com/J535D165/recordlinkage/b93d97641952f8c85106be5794ca93b1f1298fbc/docs/ref-classifiers.rst；采集：2026-11-20T08:36:09.602036+00:00；REF_DOC；范围：Toolkit API documentation, generated API bodies not fetched。

原件：`server-identity-reference/sources/recordlinkage-classifiers.raw`；SHA256 `4c602affa050356cf60c9bdd131a83aeeb1be5954c1c5361f6a172fe2e20a09f`。正文：`server-identity-reference/sources/recordlinkage-classifiers.raw` L7–16，SHA256 `4c602affa050356cf60c9bdd131a83aeeb1be5954c1c5361f6a172fe2e20a09f`。许可/用途：BSD-3-Clause。

```text

Classification is the step in the record linkage process were record pairs are
classified into matches, non-matches and possible matches [Christen2012]_.
Classification algorithms can be supervised or unsupervised (with or without
training data).


.. seealso::

    .. [Christen2012] Christen, Peter. 2012. Data matching: concepts and
```


### SIR10 · 公开测试集入口不等于真实跨设备账号真值数据；数据许可另核验

来源：https://raw.githubusercontent.com/J535D165/recordlinkage/b93d97641952f8c85106be5794ca93b1f1298fbc/docs/ref-datasets.rst；采集：2026-11-20T08:36:09.603036+00:00；REF_DOC；范围：Dataset documentation only; no rows downloaded。

原件：`server-identity-reference/sources/recordlinkage-datasets.raw`；SHA256 `d35ff7da19ea80f03383042cbbadabf4b57912b442ef783e875749716abd958a`。正文：`server-identity-reference/sources/recordlinkage-datasets.raw` L4–14，SHA256 `d35ff7da19ea80f03383042cbbadabf4b57912b442ef783e875749716abd958a`。许可/用途：BSD-3-Clause repository; underlying datasets not automatically covered。

```text

The Python Record Linkage Toolkit contains several open public datasets. Four
datasets were generated by the developers of Febrl. In the future, we are
developing tools to generate your own datasets.

.. autofunction:: recordlinkage.datasets.load_krebsregister

.. autofunction:: recordlinkage.datasets.load_febrl1

.. autofunction:: recordlinkage.datasets.load_febrl2

```


### SIR11 · 默认事件时间过滤仍可能让回填/更正值泄漏；created时间需额外限制

来源：https://raw.githubusercontent.com/feast-dev/feast/1d6cfb40f47e82872a6275b96867746ca6ef5e88/docs/getting-started/concepts/point-in-time-joins.md；采集：2026-11-20T08:36:10.159806+00:00；REF_DOC；范围：Pinned Feast docs, not all backends verified。

原件：`server-identity-reference/sources/feast-point-time.raw`；SHA256 `ce3d3a52023509f3a985e2900689835550537303b6e7a72bdcc0cda5c06507a8`。正文：`server-identity-reference/sources/feast-point-time.raw` L65–85，SHA256 `ce3d3a52023509f3a985e2900689835550537303b6e7a72bdcc0cda5c06507a8`。许可/用途：Apache-2.0。

```text
## Retrieving features as of the event time

By default, point-in-time joins only constrain the feature's event timestamp. If a data source also has a `created_timestamp_column`, it is used to deduplicate rows that share an event timestamp \(the row with the highest created timestamp wins\), but it is not otherwise filtered. This means a value that was backfilled or corrected *after* an entity dataframe timestamp can still be returned for it.

To restrict retrieval to feature values that were already available at each entity row's timestamp, pass `filter_by_created_timestamp=True`:

```python
training_df = store.get_historical_features(
    entity_df=entity_df,
    features = [
        'driver_hourly_stats:trips_today',
        'driver_hourly_stats:earnings_today'
    ],
    filter_by_created_timestamp=True,
)
```

This adds a `created_timestamp <= entity_timestamp` condition to the join, so each entity dataframe row only sees feature values whose created timestamp is at or before its own timestamp. This is useful to keep backfilled values from leaking into training data, and to reproduce what the online store would have served at each event time \(assuming the created timestamp reflects when the value became available online\).

{% hint style="info" %}
Rows with a NULL created timestamp are excluded when the flag is enabled, so the column should be non-null. Not all offline stores support this flag yet; unsupported stores raise an error rather than silently ignoring it.
```


### SIR12 · created时间过滤支持依赖具体offline store，NULL会被排除

来源：https://raw.githubusercontent.com/feast-dev/feast/1d6cfb40f47e82872a6275b96867746ca6ef5e88/docs/getting-started/concepts/point-in-time-joins.md；采集：2026-11-20T08:36:10.159806+00:00；REF_DOC；范围：Flag support and null behavior per docs。

原件：`server-identity-reference/sources/feast-point-time.raw`；SHA256 `ce3d3a52023509f3a985e2900689835550537303b6e7a72bdcc0cda5c06507a8`。正文：`server-identity-reference/sources/feast-point-time.raw` L83–87，SHA256 `ce3d3a52023509f3a985e2900689835550537303b6e7a72bdcc0cda5c06507a8`。许可/用途：Apache-2.0。

```text

{% hint style="info" %}
Rows with a NULL created timestamp are excluded when the flag is enabled, so the column should be non-null. Not all offline stores support this flag yet; unsupported stores raise an error rather than silently ignoring it.
{% endhint %}

```


### SIR13 · Entity/join key为特征查找结构，不认证自然人身份

来源：https://raw.githubusercontent.com/feast-dev/feast/1d6cfb40f47e82872a6275b96867746ca6ef5e88/docs/getting-started/concepts/entity.md；采集：2026-11-20T08:36:10.161807+00:00；REF_DOC；范围：Feast entity concept。

原件：`server-identity-reference/sources/feast-entity.raw`；SHA256 `d6a67c37fe8bc56c77faed2515b1daf1ee486fc686033f0468cf8adea5fcef0a`。正文：`server-identity-reference/sources/feast-entity.raw` L4–12，SHA256 `d6a67c37fe8bc56c77faed2515b1daf1ee486fc686033f0468cf8adea5fcef0a`。许可/用途：Apache-2.0。

```text

```python
driver = Entity(name='driver', join_keys=['driver_id'])
```

The _entity name_ is used to uniquely identify the entity (for example to show in the experimental Web UI). The _join key_ is used to identify the physical primary key on which feature values should be joined together to be retrieved during feature retrieval.

Entities are used by Feast in many contexts, as we explore below:

```


### SIR14 · sub在issuer内局部唯一；必须处理issuer及合法客户端scope

来源：https://openid.net/specs/openid-connect-core-1_0.html；采集：2026-11-20T08:36:10.648731+00:00；PROTOCOL；范围：OIDC Core1.0 errata2, not advertising-platform adoption。

原件：`server-identity-reference/sources/oidc-core.raw`；SHA256 `4d016752a645e8a3c259baa4173b5a90cb6c82898ce868fc8444adde262a5aed`。正文：`server-identity-reference/sources/oidc-core.txt` L663–671，SHA256 `42fbdc978e344bc623bbe6f159618e7289b13aa7a62b1831487516f7dde7e454`。许可/用途：OIDF Notices; specification implementation/citation, not blanket code license。

```text
sub
REQUIRED.
Subject Identifier. A locally unique and never
reassigned identifier within the Issuer for the End-User,
which is intended to be consumed by the Client,
e.g., 24400320
or AItOawmwtWwcT0k51BayewNvutrJUqsvl6qs7A4.
It MUST NOT exceed 255 ASCII [RFC20] (Cerf, V., “ASCII format for Network Interchange,” October 1969.) characters in length.
The sub value is a case-sensitive string.
```


### SIR15 · pairwise sub刻意限制客户端关联；Sector规则不能绕过

来源：https://openid.net/specs/openid-connect-core-1_0.html；采集：2026-11-20T08:36:10.648731+00:00；PROTOCOL；范围：OIDC sections8/8.1; same sector exception preserved。

原件：`server-identity-reference/sources/oidc-core.raw`；SHA256 `4d016752a645e8a3c259baa4173b5a90cb6c82898ce868fc8444adde262a5aed`。正文：`server-identity-reference/sources/oidc-core.txt` L3983–3995，SHA256 `42fbdc978e344bc623bbe6f159618e7289b13aa7a62b1831487516f7dde7e454`。许可/用途：OIDF Notices。

```text
element in its discovery document.
pairwise
This provides a different sub
value to each Client, so as not to enable Clients to correlate
the End-User's activities without permission.
The OpenID Provider's Discovery document MUST list
its supported Subject Identifier types in the
subject_types_supported element.
If there is more than one type listed in the array, the Client MAY elect to
provide its preferred identifier type using the
subject_type parameter during Registration.
TOC
8.1.
```


### SIR16 · ID Token必须绑定预期audience；认证字段不可当可任意转用的全局身份

来源：https://openid.net/specs/openid-connect-core-1_0.html；采集：2026-11-20T08:36:10.648731+00:00；PROTOCOL；范围：OIDC ID Token claims; stricter resolver policy is independent design。

原件：`server-identity-reference/sources/oidc-core.raw`；SHA256 `4d016752a645e8a3c259baa4173b5a90cb6c82898ce868fc8444adde262a5aed`。正文：`server-identity-reference/sources/oidc-core.txt` L672–683，SHA256 `42fbdc978e344bc623bbe6f159618e7289b13aa7a62b1831487516f7dde7e454`。许可/用途：OIDF Notices。

```text
aud
REQUIRED.
Audience(s) that this ID Token is intended for.
It MUST contain the OAuth 2.0 client_id
of the Relying Party as an audience value.
It MAY also contain identifiers for other audiences.
In the general case,
the aud value is an array of
case-sensitive strings.
In the common special case when there is one audience,
the aud value MAY be a single
case-sensitive string.
```


### SIR17 · PROV区分实体、活动、派生与失效；描述血缘不执行删除

来源：https://www.w3.org/TR/prov-dm/；采集：2026-11-20T08:36:10.670731+00:00；PROTOCOL；范围：PROV-DM recommendation2013-04-30; not privacy-law compliance guarantee。

原件：`server-identity-reference/sources/w3c-prov.raw`；SHA256 `5c925c21bc96c285b25017c3b90d82cf74251d07713b71fcb81ca60f873c9e88`。正文：`server-identity-reference/sources/w3c-prov.txt` L829–836，SHA256 `b432d7bff7a284807c45806c779382581c03c5fbda6b6edf2da809eb7eb0eefb`。许可/用途：W3C document-use conditions。

```text
wasEndedBy(a1, e1, -, -)
5.1.8 Invalidation
Invalidation ◊ is the start of the destruction, cessation, or expiry of an existing entity by an activity. The entity is no longer available for use (or further invalidation) after invalidation. Any generation or usage of an entity precedes its invalidation.
Given that an invalidation is the start of destruction, cessation, or
expiry, it is instantaneous.
Entities have a duration. Generation marks the beginning of an entity, whereas invalidation marks its end.
An entity's lifetime can end for different reasons:
an entity was destroyed: e.g. a painting was destroyed by fire; a Web page is taken out of a site;
```


### SIR18 · 作者以记录→潜在实体的二部图处理一致性和关联不确定性

来源：https://arxiv.org/pdf/1312.4645；采集：2026-11-20T08:37:15.108608+00:00；PAPER；范围：Steorts/Hall/Fienberg; focused PDF page1 abstract; not device benchmark。

原件：`server-identity-reference/sources/bayesian-paper-pdf.raw`；SHA256 `4995fd81d43878b5805d95b918f2e5cd1499ed6d9a68b3d1495382a061f84ef8`。正文：`server-identity-reference/sources/bayesian-paper-pdf.txt` L12–23，SHA256 `c3f995b1b816db1cf71fc71f92a501a62d5999bfac72b9973c761a7ec86631dc`。许可/用途：arXiv nonexclusive-distrib/1.0; reading/citation only, no blanket redistribution/code grant。

```text
simultaneously detecting duplicate records within ﬁles. Our key innovation involves the rep-
resentation of the pattern of links between records as a bipartite graph, in which records are
directly linked to latent true individuals, and only indirectly linked to other records.
This
ﬂexible representation of the linkage structure naturally allows us to estimate the attributes of
the unique observable people in the population, calculate transitive linkage probabilities across
records (and represent this visually), and propagate the uncertainty of record linkage into later
analyses. Our method makes it particularly easy to integrate record linkage with post-processing
procedures such as logistic regression, capture-recapture, etc. Our linkage structure lends itself
to an eﬃcient, linear-time, hybrid Markov chain Monte Carlo algorithm, which overcomes many
obstacles encountered by previously record linkage approaches, despite the high-dimensional
parameter space. We illustrate our method using longitudinal data from the National Long
```


### SIR19 · 总体关系一致性与两两阈值推断不同，论文讨论传递约束

来源：https://arxiv.org/pdf/1312.4645；采集：2026-11-20T08:37:15.108608+00:00；PAPER；范围：Focused PDF page13 discussion; not replicated。

原件：`server-identity-reference/sources/bayesian-paper-pdf.raw`；SHA256 `4995fd81d43878b5805d95b918f2e5cd1499ed6d9a68b3d1495382a061f84ef8`。正文：`server-identity-reference/sources/bayesian-paper-pdf.txt` L567–576，SHA256 `c3f995b1b816db1cf71fc71f92a501a62d5999bfac72b9973c761a7ec86631dc`。许可/用途：arXiv nonexclusive-distrib/1.0; reference reading only。

```text
a thresholding strategy. Note that the true linkage structure is transitive in the following sense: if
records A and B are the same individual, and records B and C are the same individual, then records
A and C must be the same individual as well. This requirement of transitivity, however, is in no way
enforced by the simple thresholding strategy described above. Thus, a more sophisticated approach
is required if the goal is to produce an estimated linkage structure that preserves transitivity.
To this end, it is useful to deﬁne a new concept. A set of records A is a maximal matching set
(MMS) if every record in the set has the same value of λij and no record outside the set has that
value of λij. Deﬁne Ω(A, Λ) to be 1 if A is an MMS in Λ and 0 otherwise:
Ω(A, Λ) =
X
```


## 固定组件版本

| 组件 | commit | commit日期 | 版本声明 |

|---|---|---|---|

| splink | `f319070e56c5b3666ec512811ac1820070f6f2e5` | 2026-11-11T16:49:24Z | 5.0.0 (pyproject metadata at pinned commit) |

| dedupe | `3f61e79102910bd355e920a2df7e44c14c9cb247` | 2025-07-29T00:18:20Z | 3.0.3 (pyproject metadata at pinned commit) |

| recordlinkage | `b93d97641952f8c85106be5794ca93b1f1298fbc` | 2023-07-20T12:59:41Z | SCM dynamic version; commit is normative, release UNKNOWN |

| feast | `1d6cfb40f47e82872a6275b96867746ca6ef5e88` | 2026-11-19T11:13:52Z | SCM dynamic version; commit is normative, release UNKNOWN |


## 复用原件（未重新获取）

| ID | 路径 | SHA256 | 原始URL |

|---|---|---|---|

| IG72S01 | identity-graph/google-appset-guide.raw | `0cc8467649d695ddd7f62c6b5c870f2fae77c53005f0532b6e6dad4f1025be84` | https://developer.android.com/identity/app-set-id |

| IG72S02 | identity-graph/unity-upa-doc-md.raw | `855d1cbba7a24d89ac84026f09045a14c9449b43d73cf902cb2a27e41f646154` | https://docs.unity.com/en-us/authentication/unity-player-accounts.md |

| IG72S03 | identity-graph/unity-identity-management.raw | `0eceb6f88c8b4aacd70ba8b04f276abd1fddc02dcd8c86e268828373b099fbcf` | https://docs.unity.com/en-us/authentication/identity-management.md |

| IG72S05 | vector/exchange-rampid.txt | `e2124f8e22357e85d8934c612f24483367a154bf7b25a42fbabe59c5746fc818` | https://unity.com/blog/unity-exchange-rampid-addressable-buying-mobile-gaming |

| IV74S01 | identity-value74/sources/lr-match-guide.raw | `cc8b96dd3b108fd344a97691ba8b18720ee58818eb5d887a2784998071104855` | https://developers.liveramp.com/rampid-api/reference/about-liveramp-identity-resolution |

| IV74S02 | identity-value74/sources/lr-translation.raw | `21b442cb4e20d47e96830706f380a28c34656e42ec367f97f5bdcb95cca48333` | https://developers.liveramp.com/rampid-api/reference/transcode-rampids-1 |

| IV74S03 | identity-value74/sources/lr-envelope.raw | `3587d4b72a93ccac2f0893d1028fe41422a66e2572f60cb8bfcffa9630bfe2fa` | https://developers.liveramp.com/rampid-api/reference/envelope-decryption-endpoint |

| IV74S04 | identity-value74/sources/lr-envelope.raw | `3587d4b72a93ccac2f0893d1028fe41422a66e2572f60cb8bfcffa9630bfe2fa` | https://developers.liveramp.com/rampid-api/reference/envelope-decryption-endpoint |

| IV74S05 | identity-value74/sources/lr-match-metadata.raw | `32ce90a9775e2d4770e5167c62104f7f8964b2c285d2acafc6843262affc6a46` | https://developers.liveramp.com/rampid-api/reference/matchmetadata-bundle |

| IV74S06 | identity-value74/sources/lr-match-schema.raw | `710bff26cebfeea86d1c67117e2910fb7ef1907c66bb7944de4e3f5b45049ea8` | https://developers.liveramp.com/rampid-api/reference/batch-request-calls-match |

| IV74S09 | identity-value74/sources/al-ads-public.raw | `a32a318bbbf7e0d7d9b4a3e4d26e7c20acb1bdc6a64d966d553ce40ce4d86d73` | https://dash.applovin.com/p/how-applovin-shows-you-ads |

| S25 | prediction-system/applovin-job-4712559006-clean.txt | `8e343eb570d116a28cd6f5b73780858b9d27e1c54ac47f2a4b4e4e9fc792794d` | https://boards.greenhouse.io/applovin/jobs/4712559006?gh_jid=4712559006 |

| PE77S04 | production77/sources/unity-data-job.raw | `9021e7c32296f3ac5a05acba40df89dd327e3504b36b651f5ebcaadd5d8010cf` | https://unitytech.wd1.myworkdayjobs.com/Unity/job/Mountain-View-CA-USA/Senior-Staff-Machine-Learning-Engineer--Data-Infrastructure_JOBREQ-2616462-1 |

| EC78S01 | 78_身份图谱最小生产证据契约.md | `cf05f6856e28bab18c64bca2a8be69ac28bfd85bf5ef9d12d0cd433c93012832` | 本地历史规范/分析 |

| EC78S04 | 78_证据验收与升级规则.md | `a814ba665df6cd6ac7c2118eca7f81824b1c861c1266dea7ab48c42b0fadb50b` | 本地历史规范/分析 |

| AMSS05 | adjust-mechanisms/CODE_EVIDENCE.json | `3f3eab41614daf895760de69fe94aa9b1d9881f60ef63debf4af2fa1311f8451` | 本地历史规范/分析 |

| AMSS06 | adjust-mechanisms/FINDINGS.json | `e4fc9d14697e98ba3aaf2ef12019116b125d1dd33219e2460796da8e9d39036c` | 本地历史规范/分析 |

| AMSS12 | adjust-mechanisms/自主IdentityResolver最小设计建议.md | `8dc1c35bb7ff96792a0d5a95f7f2e6a986845079f08553052f6b54f798d98aa6` | 本地历史规范/分析 |

| AMSS13 | adjust-mechanisms/下一阶段授权和测试条件.md | `bf259de522d199dc891be5904cb4c1966dea77e2b0a91aee9b4fbc68ceaf4655` | 本地历史规范/分析 |


## 公开检索边界

只访问4个明确开源项目的官方仓库、所列原始文档、OIDC/W3C规格与1篇原作者论文。未用搜索引擎泛搜岗位、专利、SDK或平台隐私页；厂商/伙伴材料只复用原件。没有新的真实跨设备/游戏收入数据下载；没有新生产数据访问渠道或可升级C_graph证据。

共42份公开GET响应，详见FETCH_MANIFEST；Git树仅元数据。网络GET均不提交身份数据或凭证，不调用文档描述的服务端接口。记录HTTP成功只证明公开内容取得，不代表API/库已运行。
