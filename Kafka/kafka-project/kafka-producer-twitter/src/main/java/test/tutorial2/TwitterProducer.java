package test.tutorial2;

import com.google.common.collect.Lists;
import com.twitter.hbc.ClientBuilder;
import com.twitter.hbc.core.Client;
import com.twitter.hbc.core.Constants;
import com.twitter.hbc.core.Hosts;
import com.twitter.hbc.core.HttpHosts;
import com.twitter.hbc.core.endpoint.StatusesFilterEndpoint;
import com.twitter.hbc.core.processor.StringDelimitedProcessor;
import com.twitter.hbc.httpclient.auth.Authentication;
import com.twitter.hbc.httpclient.auth.OAuth1;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

public class TwitterProducer {

    static Logger logger = LoggerFactory.getLogger(TwitterProducer.class);
    List<String> terms = Lists.newArrayList("kafka",  "java", "bitcoin", "animation", "apple");

    public TwitterProducer() {

    }

    public static void main(String[] args) {
        new TwitterProducer().run();
    }

    public void run() {

        logger.info("Setup");

        /* Set up your blocking queues: Be sure to size these properly based on expected TPS of your stream */
        BlockingQueue<String> msgQueue = new LinkedBlockingQueue<String>(2000);

        // create a twitter client
        Client client = createTweeterClient(msgQueue);

        // Attempts to establish a connection.
        client.connect();

        // create a kafka producer
        KafkaProducer<String, String> producer = createKafkaProducer();

        // add a shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(()->{
            logger.info("Stopping Application");
            logger.info("Shutting down client from twitter");
            client.stop();
            logger.info("Shutting down producer");
            producer.close();
            logger.info("Done");
        }));

        // loop to send tweets to kafka
        while (!client.isDone()) {
            String msg = null;
            try {
                msg = msgQueue.poll(5, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
                client.stop();
            }
            if (msg != null) {
                logger.info(msg);
                producer.send(new ProducerRecord<>("twitter_tweets", null, msg), new Callback() {
                    @Override
                    public void onCompletion(RecordMetadata recordMetadata, Exception e) {
                        if(e != null){
                            logger.error("Something bad happened", e);
                        }
                    }
                });
            }
        }
        logger.info("End of the application");
    }

    private Client createTweeterClient(BlockingQueue<String> msgQueue) {
        Properties prop = getProperties();

        /* Declare the host you want to connect to, the endpoint, and authentication (basic auth or oauth) */
        Hosts hosebirdHosts = new HttpHosts(Constants.STREAM_HOST);
        StatusesFilterEndpoint hosebirdEndpoint = new StatusesFilterEndpoint();

        hosebirdEndpoint.trackTerms(terms);

        // These secrets should be read from a config.properties file
        Authentication hosebirdAuth = new OAuth1(
                prop.getProperty("ConsumerKey"),
                prop.getProperty("ConsumerSecret"),
                prop.getProperty("AccessToken"),
                prop.getProperty("AccessSecret"));

        ClientBuilder builder = new ClientBuilder()
                .name("Hosebird-Client-01")                              // optional: mainly for the logs
                .hosts(hosebirdHosts)
                .authentication(hosebirdAuth)
                .endpoint(hosebirdEndpoint)
                .processor(new StringDelimitedProcessor(msgQueue));
        return builder.build();
    }

    private Properties getProperties() {
        String f = "config.properties";
        Properties props = new Properties();
        try {
            props.load(new java.io.FileInputStream(f));
        } catch (IOException e) {
            e.printStackTrace();
        }
        return props;
    }

    private KafkaProducer<String, String> createKafkaProducer(){
        String bootstrapServers = "127.0.0.1:9092";
        // create Producer properties
        Properties properties = new Properties();
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrapServers);
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // create safe Producer
        properties.setProperty(ProducerConfig.ENABLE_IDEMPOTENCE_CONFIG, "true");
        properties.setProperty(ProducerConfig.ACKS_CONFIG, "all");
        properties.setProperty(ProducerConfig.RETRIES_CONFIG, Integer.toString(Integer.MAX_VALUE));
        properties.setProperty(ProducerConfig.MAX_IN_FLIGHT_REQUESTS_PER_CONNECTION, "5");

        // high throughput producer (at the expense of a bit of latency and CPU usage)
        properties.setProperty(ProducerConfig.COMPRESSION_TYPE_CONFIG, "snappy");
        properties.setProperty(ProducerConfig.LINGER_MS_CONFIG, "20");
        properties.setProperty(ProducerConfig.BATCH_SIZE_CONFIG, Integer.toString(32*1024)); // 32KB

        // create the producer
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(properties);
        return producer;
    }
}
