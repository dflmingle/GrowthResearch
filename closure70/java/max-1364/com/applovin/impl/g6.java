package com.applovin.impl;

import android.net.Uri;
import android.net.Uri$Builder;
import com.applovin.impl.mediation.MaxErrorImpl;
import com.applovin.impl.sdk.utils.CollectionUtils;
import com.applovin.impl.sdk.utils.JsonUtils;
import com.applovin.impl.sdk.utils.StringUtils;
import com.applovin.mediation.MaxError;
import com.applovin.mediation.MaxReward;
import com.applovin.mediation.adapter.MaxAdapterError;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import org.json.JSONException;
import org.json.JSONObject;

/* JADX INFO: loaded from: classes.jar:com/applovin/impl/g6.class */
public class g6 extends n5 {
    private final String g;
    private final List h;
    private final o3 i;
    private final Map j;
    private final Map k;
    private final Map l;
    private final MaxError m;

    public g6(String str, List list, Map map, Map map2, MaxError maxError, o3 o3Var, com.applovin.impl.sdk.l lVar, boolean z) {
        MaxError maxError2;
        super("TaskFireMediationPostbacks", lVar);
        this.g = str + "_urls";
        this.h = list;
        this.j = u7.a(map, lVar);
        if (map2 == null) {
            map2 = map;
            HashMap map3 = new HashMap();
        }
        this.k = map2;
        if (maxError != null) {
            maxError2 = maxError;
        } else {
            maxError2 = maxErrorImpl;
            MaxErrorImpl maxErrorImpl = new MaxErrorImpl(-1);
        }
        this.m = maxError2;
        this.i = o3Var;
        HashMap map4 = new HashMap(7);
        map4.put("AppLovin-Event-Type", str);
        if (z && o3Var != null) {
            map4.put("AppLovin-Ad-Network-Name", o3Var.c());
        }
        if (o3Var instanceof c3) {
            c3 c3Var = (c3) o3Var;
            map4.put("AppLovin-Ad-Unit-Id", c3Var.getAdUnitId());
            map4.put("AppLovin-Ad-Format", c3Var.getFormat().getLabel());
            if (z) {
                map4.put("AppLovin-Third-Party-Ad-Placement-Id", c3Var.U());
            }
        }
        if (maxError != null) {
            map4.put("AppLovin-Error-Code", String.valueOf(maxError.getCode()));
            map4.put("AppLovin-Error-Message", maxError.getMessage());
        }
        this.l = map4;
    }

    private void a(String str, Map map) {
        b().h0().e(com.applovin.impl.sdk.network.d.b().d(str).c("POST").a(this.l).a(false).c(map).c(((Boolean) this.a.a(v3.P8)).booleanValue()).a());
    }

    private List f() {
        List list = this.h;
        if (list != null) {
            return list;
        }
        o3 o3Var = this.i;
        if (o3Var != null) {
            return o3Var.b(this.g);
        }
        return null;
    }

    private Map e() {
        try {
            return JsonUtils.toStringMap(new JSONObject((String) this.a.a(v3.L7)));
        } catch (JSONException unused) {
            return Collections.EMPTY_MAP;
        }
    }

    private String b(String str, Map map) {
        for (String str2 : map.keySet()) {
            str = str.replace(str2, StringUtils.emptyIfNull((String) map.get(str2)));
        }
        return str;
    }

    private h g() {
        o3 o3Var = this.i;
        if (o3Var instanceof c3) {
            return ((c3) o3Var).Q().f();
        }
        if (o3Var instanceof i5) {
            return ((i5) o3Var).u().f();
        }
        return null;
    }

    @Override // java.lang.Runnable
    public void run() {
        List listF = f();
        if (CollectionUtils.isEmpty(listF)) {
            return;
        }
        Map mapE = e();
        Iterator it = listF.iterator();
        while (it.hasNext()) {
            Uri uri = Uri.parse(a(b((String) it.next(), this.j), this.m));
            Uri$Builder uri$BuilderClearQuery = uri.buildUpon().clearQuery();
            HashMap map = new HashMap(this.k);
            for (String str : uri.getQueryParameterNames()) {
                String queryParameter = uri.getQueryParameter(str);
                if (mapE.containsKey(queryParameter)) {
                    o3 o3Var = this.i;
                    if (o3Var != null) {
                        map.put(str, o3Var.a((String) mapE.get(queryParameter)));
                    }
                } else {
                    uri$BuilderClearQuery.appendQueryParameter(str, queryParameter);
                }
            }
            Map mapE2 = this.a.B().e();
            for (String str2 : mapE2.keySet()) {
                if (map.containsKey(str2)) {
                    map.put(str2, mapE2.get(str2));
                }
            }
            h hVarG = g();
            if (hVarG != null) {
                map.put("arn_info", hVarG.e());
            }
            a(uri$BuilderClearQuery.build().toString(), map);
        }
    }

    private String a(String str, MaxError maxError) {
        int mediatedNetworkErrorCode = 0;
        String mediatedNetworkErrorMessage = MaxReward.DEFAULT_LABEL;
        if (maxError instanceof MaxAdapterError) {
            MaxAdapterError maxAdapterError = (MaxAdapterError) maxError;
            mediatedNetworkErrorCode = maxAdapterError.getMediatedNetworkErrorCode();
            mediatedNetworkErrorMessage = maxAdapterError.getMediatedNetworkErrorMessage();
        }
        return str.replace("{ERROR_CODE}", String.valueOf(maxError.getCode())).replace("{ERROR_MESSAGE}", StringUtils.encodeUriString(maxError.getMessage())).replace("{THIRD_PARTY_SDK_ERROR_CODE}", String.valueOf(mediatedNetworkErrorCode)).replace("{THIRD_PARTY_SDK_ERROR_MESSAGE}", StringUtils.encodeUriString(mediatedNetworkErrorMessage));
    }
}