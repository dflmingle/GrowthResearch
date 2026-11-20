package com.unity3d.ads.core.domain;

import com.google.protobuf.ByteString;
import com.unity3d.ads.MediationInfo;
import com.unity3d.ads.core.data.model.LoadConfigurationInternal;
import gatewayprotocol.v1.AdFormatOuterClass$AdFormat;
import gatewayprotocol.v1.AdPlayerConfigRequestKt$Dsl;
import gatewayprotocol.v1.AdPlayerConfigRequestKt$Dsl$Companion;
import gatewayprotocol.v1.AdPlayerConfigRequestOuterClass$AdPlayerConfigRequest;
import gatewayprotocol.v1.AdPlayerConfigRequestOuterClass$AdPlayerConfigRequest$Builder;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import gatewayprotocol.v1.UniversalRequestKt;
import gatewayprotocol.v1.UniversalRequestKt$PayloadKt$Dsl;
import gatewayprotocol.v1.UniversalRequestKt$PayloadKt$Dsl$Companion;
import gatewayprotocol.v1.UniversalRequestOuterClass$UniversalRequest;
import gatewayprotocol.v1.UniversalRequestOuterClass$UniversalRequest$Payload;
import gatewayprotocol.v1.UniversalRequestOuterClass$UniversalRequest$Payload$Builder;
import kotlin.Metadata;
import kotlin.coroutines.Continuation;
import kotlin.jvm.internal.Intrinsics;
import kotlin.jvm.internal.SourceDebugExtension;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/* JADX INFO: compiled from: AndroidGetAdPlayerConfigRequest.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000:\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u000e\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\b\u0000\u0018\u00002\u00020\u0001B\u0015\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005¢\u0006\u0002\u0010\u0006J=\u0010\u0007\u001a\u00020\b2\u0006\u0010\t\u001a\u00020\n2\u0006\u0010\u000b\u001a\u00020\f2\u0006\u0010\r\u001a\u00020\f2\b\u0010\u000e\u001a\u0004\u0018\u00010\u000f2\b\u0010\u0010\u001a\u0004\u0018\u00010\u0011H\u0096Bø\u0001\u0000¢\u0006\u0002\u0010\u0012R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006\u0013"}, d2 = {"Lcom/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest;", "Lcom/unity3d/ads/core/domain/GetAdPlayerConfigRequest;", "getUniversalRequestForPayLoad", "Lcom/unity3d/ads/core/domain/GetUniversalRequestForPayLoad;", "mediationInfoConverter", "Lcom/unity3d/ads/core/domain/MediationInfoConverter;", "(Lcom/unity3d/ads/core/domain/GetUniversalRequestForPayLoad;Lcom/unity3d/ads/core/domain/MediationInfoConverter;)V", "invoke", "Lgatewayprotocol/v1/UniversalRequestOuterClass$UniversalRequest;", "placement", "", "opportunityId", "Lcom/google/protobuf/ByteString;", "configToken", "adFormat", "Lgatewayprotocol/v1/AdFormatOuterClass$AdFormat;", "loadConfiguration", "Lcom/unity3d/ads/core/data/model/LoadConfigurationInternal;", "(Ljava/lang/String;Lcom/google/protobuf/ByteString;Lcom/google/protobuf/ByteString;Lgatewayprotocol/v1/AdFormatOuterClass$AdFormat;Lcom/unity3d/ads/core/data/model/LoadConfigurationInternal;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "unity-ads_defaultRelease"})
@SourceDebugExtension({"SMAP\nAndroidGetAdPlayerConfigRequest.kt\nKotlin\n*S Kotlin\n*F\n+ 1 AndroidGetAdPlayerConfigRequest.kt\ncom/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest\n+ 2 AdPlayerConfigRequestKt.kt\ngatewayprotocol/v1/AdPlayerConfigRequestKtKt\n+ 3 fake.kt\nkotlin/jvm/internal/FakeKt\n+ 4 UniversalRequestKt.kt\ngatewayprotocol/v1/UniversalRequestKt\n*L\n1#1,44:1\n10#2:45\n1#3:46\n1#3:47\n1#3:49\n484#4:48\n*S KotlinDebug\n*F\n+ 1 AndroidGetAdPlayerConfigRequest.kt\ncom/unity3d/ads/core/domain/AndroidGetAdPlayerConfigRequest\n*L\n23#1:45\n23#1:46\n38#1:49\n38#1:48\n*E\n"})
public final class AndroidGetAdPlayerConfigRequest implements GetAdPlayerConfigRequest {

    @NotNull
    private final GetUniversalRequestForPayLoad getUniversalRequestForPayLoad;

    @NotNull
    private final MediationInfoConverter mediationInfoConverter;

    public AndroidGetAdPlayerConfigRequest(@NotNull GetUniversalRequestForPayLoad getUniversalRequestForPayLoad, @NotNull MediationInfoConverter mediationInfoConverter) {
        Intrinsics.checkNotNullParameter(getUniversalRequestForPayLoad, "getUniversalRequestForPayLoad");
        Intrinsics.checkNotNullParameter(mediationInfoConverter, "mediationInfoConverter");
        this.getUniversalRequestForPayLoad = getUniversalRequestForPayLoad;
        this.mediationInfoConverter = mediationInfoConverter;
    }

    @Override // com.unity3d.ads.core.domain.GetAdPlayerConfigRequest
    @Nullable
    public Object invoke(@NotNull String placement, @NotNull ByteString opportunityId, @NotNull ByteString configToken, @Nullable AdFormatOuterClass$AdFormat adFormat, @Nullable LoadConfigurationInternal loadConfiguration, @NotNull Continuation<? super UniversalRequestOuterClass$UniversalRequest> continuation) {
        AdPlayerConfigRequestKt$Dsl$Companion adPlayerConfigRequestKt$Dsl$Companion = AdPlayerConfigRequestKt$Dsl.Companion;
        AdPlayerConfigRequestOuterClass$AdPlayerConfigRequest$Builder adPlayerConfigRequestOuterClass$AdPlayerConfigRequest$BuilderNewBuilder = AdPlayerConfigRequestOuterClass$AdPlayerConfigRequest.newBuilder();
        Intrinsics.checkNotNullExpressionValue(adPlayerConfigRequestOuterClass$AdPlayerConfigRequest$BuilderNewBuilder, "newBuilder()");
        AdPlayerConfigRequestKt$Dsl $this$adPlayerConfigRequest_u24lambda_u240$iv = adPlayerConfigRequestKt$Dsl$Companion._create(adPlayerConfigRequestOuterClass$AdPlayerConfigRequest$BuilderNewBuilder);
        $this$adPlayerConfigRequest_u24lambda_u240$iv.setConfigurationToken(configToken);
        $this$adPlayerConfigRequest_u24lambda_u240$iv.setPlacementId(placement);
        $this$adPlayerConfigRequest_u24lambda_u240$iv.setImpressionOpportunityId(opportunityId);
        if (adFormat != null) {
            $this$adPlayerConfigRequest_u24lambda_u240$iv.setAdFormat(adFormat);
        }
        if (loadConfiguration != null) {
            String p0 = loadConfiguration.getMediationAdUnitId();
            if (p0 != null) {
                new AndroidGetAdPlayerConfigRequest$invoke$request$1$2$2($this$adPlayerConfigRequest_u24lambda_u240$iv).set(p0);
            }
            MediationInfo mediationInfoData = loadConfiguration.getMediationInfo();
            if (mediationInfoData != null) {
                $this$adPlayerConfigRequest_u24lambda_u240$iv.setMediationInfo(this.mediationInfoConverter.invoke(mediationInfoData));
            }
            $this$adPlayerConfigRequest_u24lambda_u240$iv.putAllExtras($this$adPlayerConfigRequest_u24lambda_u240$iv.getExtrasMap(), loadConfiguration.getExtras());
        }
        AdPlayerConfigRequestOuterClass$AdPlayerConfigRequest request = $this$adPlayerConfigRequest_u24lambda_u240$iv._build();
        UniversalRequestKt universalRequestKt = UniversalRequestKt.INSTANCE;
        UniversalRequestKt$PayloadKt$Dsl$Companion universalRequestKt$PayloadKt$Dsl$Companion = UniversalRequestKt$PayloadKt$Dsl.Companion;
        UniversalRequestOuterClass$UniversalRequest$Payload$Builder universalRequestOuterClass$UniversalRequest$Payload$BuilderNewBuilder = UniversalRequestOuterClass$UniversalRequest$Payload.newBuilder();
        Intrinsics.checkNotNullExpressionValue(universalRequestOuterClass$UniversalRequest$Payload$BuilderNewBuilder, "newBuilder()");
        UniversalRequestKt$PayloadKt$Dsl $this$payload_u24lambda_u241$iv = universalRequestKt$PayloadKt$Dsl$Companion._create(universalRequestOuterClass$UniversalRequest$Payload$BuilderNewBuilder);
        $this$payload_u24lambda_u241$iv.setAdPlayerConfigRequest(request);
        UniversalRequestOuterClass$UniversalRequest$Payload payload = $this$payload_u24lambda_u241$iv._build();
        return this.getUniversalRequestForPayLoad.invoke(payload, continuation);
    }
}