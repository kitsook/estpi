import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class EstimatePiFuture {
    final static long TOTAL_ROUNDS = (long)Math.pow(10, 10);

    public static void main(String[] args) {
        int numOfCores = Runtime.getRuntime().availableProcessors();
        int numOfThreads = Math.max(2, numOfCores);
        ExecutorService executorService = Executors.newFixedThreadPool(numOfThreads);

        long[] roundsPerThread = new long[numOfThreads];
        for (int i=0; i < numOfThreads-1; i++) {
            roundsPerThread[i] = TOTAL_ROUNDS / numOfThreads;
        }
        roundsPerThread[numOfThreads-1] = TOTAL_ROUNDS - ((numOfThreads-1) * (TOTAL_ROUNDS / numOfThreads));

        long start = System.currentTimeMillis();
        List<CompletableFuture<Long>> childFutures = new ArrayList<>();
        for (int i = 0; i < numOfThreads; i++) {
            final int slot = i;

            childFutures.add(
                CompletableFuture
                    .supplyAsync(() -> roundsPerThread[slot])
                    .thenApplyAsync((l) -> {
                        long inCircleCount = 0;
                        Random rand = new Random();

                        for (long j = 0; j < l; j++) {
                            double x = rand.nextDouble();
                            double y = rand.nextDouble();
                            double dist = Math.sqrt(x * x + y * y);
                            if (dist <= 1.0) {
                                inCircleCount += 1;
                            }
                        }
                        return inCircleCount;

                    }, executorService));
        }

        try {
            long count = childFutures.stream()
                .map(f -> f.join())
                .reduce(0L, Long::sum);
            long end = System.currentTimeMillis();
            System.out.format("Estimated value of pi is %f\n", 4.0 * ((double)count / TOTAL_ROUNDS));
            System.out.format("Time taken: %.2fs\n", (end-start) / 1000.0);
        } catch (Exception e) {
            e.printStackTrace(System.err);
        }

        executorService.shutdown();
    }
    // Estimated value of pi is 3.141618
    // Time taken: 96.90s
}