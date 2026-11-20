package com.unity3d.ads.core.domain;

import android.content.Context;
import com.unity3d.ads.UnityAdsShowOptions;
import com.unity3d.ads.adplayer.AdPlayer;
import com.unity3d.ads.core.configuration.GameServerIdReader;
import com.unity3d.ads.core.data.model.AdObject;
import com.unity3d.ads.core.data.model.ShowEvent;
import com.unity3d.ads.core.data.repository.AdRepository;
import gatewayprotocol.v1.DiagnosticEventRequestOuterClass$DiagnosticEventType;
import kotlin.Metadata;
import kotlin.Unit;
import kotlin.coroutines.Continuation;
import kotlin.coroutines.intrinsics.IntrinsicsKt;
import kotlin.jvm.internal.Intrinsics;
import kotlinx.coroutines.flow.Flow;
import kotlinx.coroutines.flow.FlowKt;
import org.jetbrains.annotations.NotNull;
import org.jetbrains.annotations.Nullable;

/* JADX INFO: compiled from: AndroidShow.kt */
/* JADX INFO: loaded from: classes.jar:com/unity3d/ads/core/domain/AndroidShow.class */
@Metadata(mv = {1, 8, 0}, k = 1, xi = DiagnosticEventRequestOuterClass$DiagnosticEventType.DIAGNOSTIC_EVENT_TYPE_NATIVE_AD_QUALITY_INIT_STARTED_VALUE, d1 = {"\u0000N\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0002\b\u0002\n\u0002\u0018\u0002\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0018\u0002\n\u0000\n\u0002\u0010\u0002\n\u0002\b\u0002\b\u0000\u0018\u00002\u00020\u0001B5\u0012\u0006\u0010\u0002\u001a\u00020\u0003\u0012\u0006\u0010\u0004\u001a\u00020\u0005\u0012\u0006\u0010\u0006\u001a\u00020\u0007\u0012\u0006\u0010\b\u001a\u00020\t\u0012\u0006\u0010\n\u001a\u00020\u000b\u0012\u0006\u0010\f\u001a\u00020\r¢\u0006\u0002\u0010\u000eJ!\u0010\u000f\u001a\b\u0012\u0004\u0012\u00020\u00110\u00102\u0006\u0010\u0012\u001a\u00020\u00132\b\u0010\u0014\u001a\u0004\u0018\u00010\u0015H\u0096\u0002J\u0019\u0010\u0016\u001a\u00020\u00172\u0006\u0010\u0012\u001a\u00020\u0013H\u0096@ø\u0001\u0000¢\u0006\u0002\u0010\u0018R\u000e\u0010\u0004\u001a\u00020\u0005X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0002\u001a\u00020\u0003X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\u0006\u001a\u00020\u0007X\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\f\u001a\u00020\rX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\b\u001a\u00020\tX\u0082\u0004¢\u0006\u0002\n\u0000R\u000e\u0010\n\u001a\u00020\u000bX\u0082\u0004¢\u0006\u0002\n\u0000\u0082\u0002\u0004\n\u0002\b\u0019¨\u0006\u0019"}, d2 = {"Lcom/unity3d/ads/core/domain/AndroidShow;", "Lcom/unity3d/ads/core/domain/Show;", "context", "Landroid/content/Context;", "adRepository", "Lcom/unity3d/ads/core/data/repository/AdRepository;", "gameServerIdReader", "Lcom/unity3d/ads/core/configuration/GameServerIdReader;", "sendDiagnosticEvent", "Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;", "validateExtrasSize", "Lcom/unity3d/ads/core/domain/ValidateExtrasSize;", "handleGatewayAdResponse", "Lcom/unity3d/ads/core/domain/HandleGatewayAdResponse;", "(Landroid/content/Context;Lcom/unity3d/ads/core/data/repository/AdRepository;Lcom/unity3d/ads/core/configuration/GameServerIdReader;Lcom/unity3d/ads/core/domain/SendDiagnosticEvent;Lcom/unity3d/ads/core/domain/ValidateExtrasSize;Lcom/unity3d/ads/core/domain/HandleGatewayAdResponse;)V", "invoke", "Lkotlinx/coroutines/flow/Flow;", "Lcom/unity3d/ads/core/data/model/ShowEvent;", "adObject", "Lcom/unity3d/ads/core/data/model/AdObject;", "showOptions", "Lcom/unity3d/ads/UnityAdsShowOptions;", "terminate", "", "(Lcom/unity3d/ads/core/data/model/AdObject;Lkotlin/coroutines/Continuation;)Ljava/lang/Object;", "unity-ads_defaultRelease"})
public final class AndroidShow implements Show {

    @NotNull
    private final Context context;

    @NotNull
    private final AdRepository adRepository;

    @NotNull
    private final GameServerIdReader gameServerIdReader;

    @NotNull
    private final SendDiagnosticEvent sendDiagnosticEvent;

    @NotNull
    private final ValidateExtrasSize validateExtrasSize;

    @NotNull
    private final HandleGatewayAdResponse handleGatewayAdResponse;

    public AndroidShow(@NotNull Context context, @NotNull AdRepository adRepository, @NotNull GameServerIdReader gameServerIdReader, @NotNull SendDiagnosticEvent sendDiagnosticEvent, @NotNull ValidateExtrasSize validateExtrasSize, @NotNull HandleGatewayAdResponse handleGatewayAdResponse) {
        Intrinsics.checkNotNullParameter(context, "context");
        Intrinsics.checkNotNullParameter(adRepository, "adRepository");
        Intrinsics.checkNotNullParameter(gameServerIdReader, "gameServerIdReader");
        Intrinsics.checkNotNullParameter(sendDiagnosticEvent, "sendDiagnosticEvent");
        Intrinsics.checkNotNullParameter(validateExtrasSize, "validateExtrasSize");
        Intrinsics.checkNotNullParameter(handleGatewayAdResponse, "handleGatewayAdResponse");
        this.context = context;
        this.adRepository = adRepository;
        this.gameServerIdReader = gameServerIdReader;
        this.sendDiagnosticEvent = sendDiagnosticEvent;
        this.validateExtrasSize = validateExtrasSize;
        this.handleGatewayAdResponse = handleGatewayAdResponse;
    }

    public static final /* synthetic */ AdRepository access$getAdRepository$p(AndroidShow $this) {
        return $this.adRepository;
    }

    public static final /* synthetic */ SendDiagnosticEvent access$getSendDiagnosticEvent$p(AndroidShow $this) {
        return $this.sendDiagnosticEvent;
    }

    public static final /* synthetic */ HandleGatewayAdResponse access$getHandleGatewayAdResponse$p(AndroidShow $this) {
        return $this.handleGatewayAdResponse;
    }

    public static final /* synthetic */ Context access$getContext$p(AndroidShow $this) {
        return $this.context;
    }

    public static final /* synthetic */ GameServerIdReader access$getGameServerIdReader$p(AndroidShow $this) {
        return $this.gameServerIdReader;
    }

    public static final /* synthetic */ ValidateExtrasSize access$getValidateExtrasSize$p(AndroidShow $this) {
        return $this.validateExtrasSize;
    }

    @Override // com.unity3d.ads.core.domain.Show
    @NotNull
    public Flow<ShowEvent> invoke(@NotNull AdObject adObject, @Nullable UnityAdsShowOptions showOptions) {
        Intrinsics.checkNotNullParameter(adObject, "adObject");
        return FlowKt.flow(new AndroidShow$invoke$1(adObject, this, showOptions, null));
    }

    @Override // com.unity3d.ads.core.domain.Show
    @Nullable
    public Object terminate(@NotNull AdObject adObject, @NotNull Continuation<? super Unit> continuation) {
        AdPlayer adPlayer = adObject.getAdPlayer();
        if (adPlayer == null) {
            return Unit.INSTANCE;
        }
        Object objDestroy = adPlayer.destroy(continuation);
        return objDestroy == IntrinsicsKt.getCOROUTINE_SUSPENDED() ? objDestroy : Unit.INSTANCE;
    }
}