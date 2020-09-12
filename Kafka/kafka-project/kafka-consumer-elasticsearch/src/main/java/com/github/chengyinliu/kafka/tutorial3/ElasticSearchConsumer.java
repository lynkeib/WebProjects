package com.github.chengyinliu.kafka.tutorial3;

import com.google.gson.JsonParser;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.lucene.index.IndexReader;
import org.elasticsearch.action.bulk.BulkRequest;
import org.elasticsearch.action.bulk.BulkResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContent;
import org.elasticsearch.common.xcontent.XContentType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.time.Duration;
import java.util.Arrays;
import java.util.Properties;

public class ElasticSearchConsumer {

    private static Logger logger = LoggerFactory.getLogger(ElasticSearchConsumer.class);
    private static JsonParser jsonParser = new JsonParser();

    public static RestHighLevelClient createClient() {
        Properties prop = getProperties();
        System.out.println(prop.getProperty("host_name"));
        System.out.println(prop.getProperty("username"));
        System.out.println(prop.getProperty("password"));
        String hostname = prop.getProperty("host_name");
        String username = prop.getProperty("username");
        String password = prop.getProperty("password");

        final CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(username, password));

        RestClientBuilder builder = RestClient.builder(new HttpHost(hostname, 443, "https")).setHttpClientConfigCallback(new RestClientBuilder.HttpClientConfigCallback() {
            @Override
            public HttpAsyncClientBuilder customizeHttpClient(HttpAsyncClientBuilder httpAsyncClientBuilder) {
                return httpAsyncClientBuilder.setDefaultCredentialsProvider(credentialsProvider);
            }
        });

        RestHighLevelClient restClient = new RestHighLevelClient(builder);
        return restClient;
    }

    private static KafkaConsumer<String, String> createConsumer(String topic) {
        String bootstrapServer = "127.0.0.1:9092";
        String groupId = "kafka-consumer-elasticsearch";
//        String topic = "twitter_tweets";

        // create consumer config.properties
        Properties properties = new Properties();
        properties.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServer);
        properties.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        properties.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        properties.setProperty(ConsumerConfig.ENABLE_AUTO_COMMIT_CONFIG, "false");
        properties.setProperty(ConsumerConfig.MAX_POLL_RECORDS_CONFIG, "100");

        // create consumer
        KafkaConsumer<String, String> consumer = new KafkaConsumer<String, String>(properties);
        consumer.subscribe(Arrays.asList(topic));
        return consumer;
    }

    public static void main(String[] args) throws IOException {
        RestHighLevelClient client = createClient();
//        String jsonString = "{\"foo\":\"bar\"}";


        KafkaConsumer<String, String> consumer = createConsumer("twitter_tweets");
        while (true) {
            ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));

            int recordsCount = records.count();
            logger.info("Received " + recordsCount + " records");

            BulkRequest bulkRequest = new BulkRequest();

            for (ConsumerRecord<String, String> record : records) {
//                logger.info("Key: " + record.key() + ", Value: " + record.value());
//                logger.info("Partition: " + record.partition() + ", Offset: " + record.offset());

                // 2 strategies to generate Unique ID for each record
                // kafka generic ID
//                String id = record.topic() + "_" + record.partition() + "_" + record.offset();

                // twitter feed specific id
                try{
                    String id = extractIdFromTweet(record.value());
                    String jsonString = record.value();
                    IndexRequest indexRequest = new IndexRequest("twitter", "tweets", id).source(jsonString, XContentType.JSON);

                    bulkRequest.add(indexRequest);
                }catch(NullPointerException e){
                    logger.warn("skipping bad data: " + record.value());
                }




//                IndexResponse indexResponse = client.index(indexRequest, RequestOptions.DEFAULT);
//                logger.info(indexResponse.getId());


//                try {
//                    Thread.sleep(10);
//                } catch (InterruptedException e) {
//                    e.printStackTrace();
//                }
            }
            if(recordsCount > 0){
                BulkResponse bulkResponse = client.bulk(bulkRequest, RequestOptions.DEFAULT);
                logger.info("Committing offsets ... ");
                consumer.commitSync();
                logger.info("Offsets have been committed... ");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        }
//        client.close();
    }

    private static String extractIdFromTweet(String tweetJson) {
        return jsonParser.parse(tweetJson).getAsJsonObject().get("id_str").getAsString();
    }

    private static Properties getProperties() {
        String f = "config.properties";
        Properties props = new Properties();
        try {
            props.load(new java.io.FileInputStream(f));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return props;
    }
}
