package com.example.smartcart;

import android.content.Context;
import android.util.Log;

import androidx.annotation.Nullable;

import com.android.volley.NetworkResponse;
import com.android.volley.ParseError;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.JsonArrayRequest;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.JsonRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;

public class Connector {

    private static final String HOST = "http://preljevstoga-smartcart.herokuapp.com/";

    private static Connector singleInstance;
    private static RequestQueue requestQueue;
    private static Context appContext;

    private Connector(Context c) {
        appContext = c;
        requestQueue = getRequestQueue();
    }

    public static RequestQueue getRequestQueue() {
        if (requestQueue == null) {
            requestQueue = Volley.newRequestQueue(appContext);
        }
        return requestQueue;
    }

    public static Connector getInstance(Context c) {
        if (singleInstance == null) {
            singleInstance = new Connector(c.getApplicationContext());
        }
        return singleInstance;
    }

    public void logIn(String email, String password, Response.Listener<JSONObject> onSuccess,
                      Response.ErrorListener onFail) {
        JSONObject jo = new JSONObject();
        try {
            jo.put("email", email);
            jo.put("password", password);
        } catch (JSONException e) {
            // za printati stacktrace napraviti stringwriter/printwriter wrapper i upisati u string
            Log.e("Login", e.toString());
        }
        String url = HOST + "android/login";
        JsonObjectRequest jor = new JsonObjectRequest(Request.Method.POST, url, jo, onSuccess, onFail);

        getRequestQueue().add(jor);
    }

    public void logOut(String sessionId, Response.Listener<JSONObject> onSuccess,
                       Response.ErrorListener onFail){
        JSONObject jo = new JSONObject();
        try {
            jo.put("sessionId", sessionId );
        } catch (JSONException e) {
            // za printati stacktrace napraviti stringwriter/printwriter wrapper i upisati u string
            Log.e("Logout", e.toString());
        }
        String url = HOST + "android/logout";
        JsonObjectRequest jor = new JsonObjectRequest(Request.Method.POST, url, jo, onSuccess, onFail);

        getRequestQueue().add(jor);

    }

    public void signUp(String email, String password, int secretCode,
                       Response.Listener<String> onSuccess, Response.ErrorListener onFail) {
        JSONObject jo = new JSONObject();
        try {
            jo.put("email", email);
            jo.put("password", password);
            jo.put("secret_code", secretCode);
        } catch (JSONException e) {
            // za printati stacktrace napraviti stringwriter/printwriter wrapper i upisati u string
            Log.e("Signup", e.toString());
        }
        String url = HOST + "android/signup";
        JsonToStringRequest jtsr = new JsonToStringRequest(Request.Method.POST, url, jo, onSuccess, onFail);
        getRequestQueue().add(jtsr);

    }

    public void fetchTrgovine( Response.Listener<String> onSuccess, Response.ErrorListener onFail) {
        JSONObject jo = new JSONObject();
        String url = HOST + "android/trgovine";
        JsonToStringRequest jtsr = new JsonToStringRequest(Request.Method.POST, url, jo, onSuccess, onFail);
        getRequestQueue().add(jtsr);
    }

    private static class JsonToStringRequest extends JsonRequest<String> {
        public JsonToStringRequest(int method, String url,
                                   JSONObject requestBody,
                                   Response.Listener<String> listener,
                                   @Nullable Response.ErrorListener errorListener
        ) {
            super(method, url, requestBody.toString(), listener, errorListener);
        }

        @Override
        protected Response<String> parseNetworkResponse(NetworkResponse response) {
            String s;
            try {
                s = new String(response.data, HttpHeaderParser.parseCharset(response.headers, "utf-8"));
            } catch (UnsupportedEncodingException e) {
                return Response.error(new ParseError(e));
            }
            return Response.success(s, HttpHeaderParser.parseCacheHeaders(response));
        }
    }

    private static class JsonToJsonArrayRequest extends JsonRequest<JSONArray> {
        public JsonToJsonArrayRequest(int method, String url,
                                   JSONObject requestBody,
                                   Response.Listener<JSONArray> listener,
                                   @Nullable Response.ErrorListener errorListener
        ) {
            super(method, url, requestBody.toString(), listener, errorListener);
        }

        @Override
        protected Response<JSONArray> parseNetworkResponse(NetworkResponse response) {
            try {
                String s =
                        new String(
                                response.data,
                                HttpHeaderParser.parseCharset(response.headers, PROTOCOL_CHARSET));
                return Response.success(
                        new JSONArray(s), HttpHeaderParser.parseCacheHeaders(response));
            } catch (UnsupportedEncodingException | JSONException e) {
                return Response.error(new ParseError(e));
            }
        }
    }
}