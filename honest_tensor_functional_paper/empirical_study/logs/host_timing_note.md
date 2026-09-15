# Host timing qualification

The primary run continued across a prolonged interactive host session. When apparent solver progress stalled, a process-status check found the study worker alive and using CPU. Its elapsed wall-clock age was far larger than its accumulated CPU time (roughly 15 hours elapsed versus 20 minutes CPU at that inspection). This observation does not identify the cause of inactive periods.

Do not interpret primary case elapsed times as uninterrupted compute costs. Individual timers and wall times can include scheduling delays. S11 separately measures fixed-thread repeated calls, reports variability and traced allocations, and is the source for the computational comparison. The host is not an isolated benchmarking server. Algorithmic node counts, tolerance statuses and output correctness are independent of interpreting elapsed time as CPU time.

No solver budget, tolerance, seed or primary configuration was removed or reduced because of the delay. No unrelated user processes were changed or stopped.
