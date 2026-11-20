package com.applovin.impl;

import android.os.Bundle;
import com.applovin.impl.sdk.utils.BundleUtils;
import com.applovin.impl.sdk.utils.JsonUtils;
import com.applovin.impl.sdk.utils.StringUtils;
import com.applovin.mediation.MaxReward;
import com.applovin.sdk.AppLovinEventParameters;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import org.json.JSONArray;
import org.json.JSONObject;

/* JADX INFO: loaded from: classes.jar:com/applovin/impl/o3.class */
public class o3 {
    protected final com.applovin.impl.sdk.l a;
    private final JSONObject b;
    protected final JSONObject d;
    private final Map f;
    private final m5 g;
    protected final m5 h;
    private String i;
    private String j;
    private final Object c = new Object();
    protected final Object e = new Object();

    public o3(Map map, JSONObject jSONObject, JSONObject jSONObject2, com.applovin.impl.sdk.l lVar) {
        if (lVar == null) {
            throw new IllegalArgumentException("No sdk specified");
        }
        if (jSONObject2 == null) {
            throw new IllegalArgumentException("No full response specified");
        }
        if (jSONObject == null) {
            throw new IllegalArgumentException("No ad object specified");
        }
        this.a = lVar;
        if (((Boolean) lVar.a(c5.N6)).booleanValue()) {
            this.g = new m5(jSONObject2);
            this.h = new m5(jSONObject);
            this.b = null;
            this.d = null;
        } else {
            this.b = jSONObject2;
            this.d = jSONObject;
            this.g = null;
            this.h = null;
        }
        this.f = map;
    }

    private int j() {
        return a("mute_state", b("mute_state", ((Integer) this.a.a(v3.r8)).intValue()));
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v4, types: [org.json.JSONObject] */
    public JSONObject g() {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a();
        }
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = r0.b;
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [boolean] */
    protected boolean d(String str) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str);
        }
        ?? Has = this;
        synchronized (Has.c) {
            try {
                Has = Has.b.has(str);
            } catch (Throwable th) {
                throw Has;
            }
        }
        return Has;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [java.lang.Boolean] */
    protected Boolean b(String str, Boolean bool) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, bool);
        }
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = JsonUtils.getBoolean(r0.b, str, bool);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [double] */
    protected double a(String str, double d) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, d);
        }
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = JsonUtils.getDouble(r0.b, str, d);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [boolean] */
    protected boolean c(String str) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str);
        }
        ?? Has = this;
        synchronized (Has.e) {
            try {
                Has = Has.d.has(str);
            } catch (Throwable th) {
                throw Has;
            }
        }
        return Has;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [java.lang.Object] */
    protected Object e(String str) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.b(str);
        }
        ?? Opt = this;
        synchronized (Opt.e) {
            try {
                Opt = Opt.d.opt(str);
            } catch (Throwable th) {
                throw Opt;
            }
        }
        return Opt;
    }

    public String getAdUnitId() {
        return b("ad_unit_id", MaxReward.DEFAULT_LABEL);
    }

    public String k() {
        return c().split("_")[0];
    }

    public boolean p() {
        return a("is_testing", Boolean.FALSE).booleanValue();
    }

    public Boolean n() {
        String str = this.a.p0().getExtraParameters().get("huc");
        if (StringUtils.isValidString(str)) {
            return Boolean.valueOf(str);
        }
        return c("huc") ? a("huc", Boolean.FALSE) : b("huc", (Boolean) null);
    }

    public Boolean o() {
        String str = this.a.p0().getExtraParameters().get("dns");
        if (StringUtils.isValidString(str)) {
            return Boolean.valueOf(str);
        }
        return c("dns") ? a("dns", Boolean.FALSE) : b("dns", (Boolean) null);
    }

    public boolean r() {
        return a("run_on_ui_thread", Boolean.TRUE).booleanValue();
    }

    public Map i() {
        return this.f;
    }

    public Bundle l() {
        Bundle bundle;
        if (e("server_parameters") instanceof JSONObject) {
            m5 m5Var = this.h;
            bundle = m5Var != null ? (Bundle) m5Var.a(m5Var2 -> {
                return JsonUtils.toBundle(m5Var2.a("server_parameters", (JSONObject) null));
            }) : JsonUtils.toBundle(a("server_parameters", (JSONObject) null));
        } else {
            bundle = bundle;
            Bundle bundle2 = new Bundle();
        }
        int iJ = j();
        if (iJ != -1) {
            if (iJ == 2) {
                bundle.putBoolean("is_muted", this.a.p0().isMuted());
            } else {
                bundle.putBoolean("is_muted", iJ == 0);
            }
        }
        if (!bundle.containsKey(AppLovinEventParameters.REVENUE_AMOUNT)) {
            bundle.putLong(AppLovinEventParameters.REVENUE_AMOUNT, b(AppLovinEventParameters.REVENUE_AMOUNT, 0L));
        }
        if (bundle.containsKey(AppLovinEventParameters.REVENUE_CURRENCY)) {
            return bundle;
        }
        Bundle bundle3 = bundle;
        bundle3.putString(AppLovinEventParameters.REVENUE_CURRENCY, b(AppLovinEventParameters.REVENUE_CURRENCY, MaxReward.DEFAULT_LABEL));
        return bundle3;
    }

    public Bundle f() {
        return BundleUtils.getBundle("custom_parameters", new Bundle(), l());
    }

    public long m() {
        return a("adapter_timeout_ms", ((Long) this.a.a(v3.N7)).longValue());
    }

    public long h() {
        return a("init_completion_delay_ms", -1L);
    }

    public boolean s() {
        return a("eagerly_initialize", Boolean.TRUE).booleanValue();
    }

    public String getPlacement() {
        return this.i;
    }

    public boolean q() {
        return a("reinitialize_if_init_fails", Boolean.FALSE).booleanValue();
    }

    public String toString() {
        return "MediationAdapterSpec{adapterClass='" + b() + "', adapterName='" + c() + "', isTesting=" + p() + '}';
    }

    public void f(String str) {
        this.j = str;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [int] */
    protected int b(String str, int i) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, i);
        }
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = JsonUtils.getInt(r0.b, str, i);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v4, types: [org.json.JSONObject] */
    protected JSONObject a() {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a();
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = r0.d;
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Object, java.lang.Throwable] */
    protected void c(String str, int i) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            m5Var.b(str, i);
            return;
        }
        ?? r0 = this.e;
        synchronized (r0) {
            try {
                JsonUtils.putInt(this.d, str, i);
            } catch (Throwable th) {
                throw r0;
            }
        }
    }

    public String d() {
        if (c("consent_string")) {
            return a("consent_string", (String) null);
        }
        if (d("consent_string")) {
            return b("consent_string", (String) null);
        }
        return this.a.t0().j();
    }

    public void g(String str) {
        this.i = str;
    }

    public String e() {
        return this.j;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [org.json.JSONArray] */
    protected JSONArray b(String str, JSONArray jSONArray) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, jSONArray);
        }
        ?? jSONArray2 = this;
        synchronized (jSONArray2.c) {
            try {
                jSONArray2 = JsonUtils.getJSONArray(jSONArray2.b, str, jSONArray);
            } catch (Throwable th) {
                throw jSONArray2;
            }
        }
        return jSONArray2;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [java.lang.Boolean] */
    protected Boolean a(String str, Boolean bool) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, bool);
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = JsonUtils.getBoolean(r0.d, str, bool);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Object, java.lang.Throwable] */
    protected void c(String str, long j) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            m5Var.b(str, j);
            return;
        }
        ?? r0 = this.e;
        synchronized (r0) {
            try {
                JsonUtils.putLong(this.d, str, j);
            } catch (Throwable th) {
                throw r0;
            }
        }
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [long] */
    protected long b(String str, long j) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, j);
        }
        ?? r0 = this;
        synchronized (r0.c) {
            try {
                r0 = JsonUtils.getLong(r0.b, str, j);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [double] */
    protected double a(String str, float f) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, f);
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = JsonUtils.getDouble(r0.d, str, f);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Object, java.lang.Throwable] */
    protected void c(String str, String str2) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            m5Var.b(str, str2);
            return;
        }
        ?? r0 = this.e;
        synchronized (r0) {
            try {
                JsonUtils.putString(this.d, str, str2);
            } catch (Throwable th) {
                throw r0;
            }
        }
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [java.lang.String] */
    protected String b(String str, String str2) {
        m5 m5Var = this.g;
        if (m5Var != null) {
            return m5Var.a(str, str2);
        }
        ?? string = this;
        synchronized (string.c) {
            try {
                string = JsonUtils.getString(string.b, str, str2);
            } catch (Throwable th) {
                throw string;
            }
        }
        return string;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [int] */
    protected int a(String str, int i) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, i);
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = JsonUtils.getInt(r0.d, str, i);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    public String c() {
        return a("name", (String) null);
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [float] */
    protected float b(String str, float f) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, f);
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = JsonUtils.getFloat(r0.d, str, f);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [org.json.JSONArray] */
    protected JSONArray a(String str, JSONArray jSONArray) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, jSONArray);
        }
        ?? jSONArray2 = this;
        synchronized (jSONArray2.e) {
            try {
                jSONArray2 = JsonUtils.getJSONArray(jSONArray2.d, str, jSONArray);
            } catch (Throwable th) {
                throw jSONArray2;
            }
        }
        return jSONArray2;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [org.json.JSONObject] */
    protected JSONObject a(String str, JSONObject jSONObject) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, jSONObject);
        }
        ?? jSONObject2 = this;
        synchronized (jSONObject2.e) {
            try {
                jSONObject2 = JsonUtils.getJSONObject(jSONObject2.d, str, jSONObject);
            } catch (Throwable th) {
                throw jSONObject2;
            }
        }
        return jSONObject2;
    }

    public String b() {
        return a("class", (String) null);
    }

    public List b(String str) {
        List listOptList;
        List listOptList2;
        if (str != null) {
            m5 m5Var = this.g;
            if (m5Var != null) {
                listOptList = m5Var.b(str, Collections.EMPTY_LIST);
            } else {
                listOptList = JsonUtils.optList(b(str, new JSONArray()), Collections.EMPTY_LIST);
            }
            m5 m5Var2 = this.h;
            if (m5Var2 != null) {
                listOptList2 = m5Var2.b(str, Collections.EMPTY_LIST);
            } else {
                listOptList2 = JsonUtils.optList(a(str, new JSONArray()), Collections.EMPTY_LIST);
            }
            ArrayList arrayList = new ArrayList(listOptList.size() + listOptList2.size());
            arrayList.addAll(listOptList);
            arrayList.addAll(listOptList2);
            return arrayList;
        }
        throw new IllegalArgumentException("No key specified");
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [long] */
    protected long a(String str, long j) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, j);
        }
        ?? r0 = this;
        synchronized (r0.e) {
            try {
                r0 = JsonUtils.getLong(r0.d, str, j);
            } catch (Throwable th) {
                throw r0;
            }
        }
        return r0;
    }

    /* JADX WARN: Multi-variable type inference failed */
    /* JADX WARN: Type inference failed for: r0v2, types: [com.applovin.impl.o3] */
    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Throwable] */
    /* JADX WARN: Type inference failed for: r0v5, types: [java.lang.String] */
    protected String a(String str, String str2) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            return m5Var.a(str, str2);
        }
        ?? string = this;
        synchronized (string.e) {
            try {
                string = JsonUtils.getString(string.d, str, str2);
            } catch (Throwable th) {
                throw string;
            }
        }
        return string;
    }

    /* JADX WARN: Type inference failed for: r0v3, types: [java.lang.Object, java.lang.Throwable] */
    protected void a(String str, Object obj) {
        m5 m5Var = this.h;
        if (m5Var != null) {
            m5Var.a(str, obj);
            return;
        }
        ?? r0 = this.e;
        synchronized (r0) {
            try {
                JsonUtils.putObject(this.d, str, obj);
            } catch (Throwable th) {
                throw r0;
            }
        }
    }

    public String a(String str) {
        String strA = a(str, MaxReward.DEFAULT_LABEL);
        return StringUtils.isValidString(strA) ? strA : b(str, MaxReward.DEFAULT_LABEL);
    }
}