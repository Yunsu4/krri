package network;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface RetrofitInterface {

    @GET("15100736/v1/uddi:877d8868-049b-45bf-9e93-e6dc1874afa4")
    Call<WeddingModel> getServiceList(
            @Query("page") int page,
            @Query("perPage") int perPage,
            @Query("serviceKey") String serviceKey
    );


}
