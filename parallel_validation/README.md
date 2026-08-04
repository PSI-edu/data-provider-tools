# Parallel Validation

## Introduction

Large bundles and collections can take an unreasonable amount of time to validate. Much of the problem seems to be that the validator does not scale well across multiple cores. Running multiple instances of the validator can help reduce the amount of time that validation requires.

## Is parallel validation right for you?

### System constraints

The most important consideration is whether you are I/O bound or CPU bound. If you are I/O bound, then parallelizing the validator won't help. You can roughly determine whether you are CPU bound by running the top command while running the validator. Look for any java processes. If you see some that are running at or near 100%, that means that the entire core is being used, and you could benefit from parallelizing the task. However, check your total CPU statistics, as well. If you don't have idle capacity, this means that all of your cores are already being fully utilized, and parallelizing won't help.

To recap, what you want to see before running parallel validation is evidence that individual cores are being fully utilized, while at the same time, there is leftover CPU capacity overall.

### Bundle size constraints

Parallel validation works better when there is a large number of products to validate. If you are validating only a small number of products, the validation will likely finish in a reasonable timeframe anyway, and there will be no point in taking the effort to parallelize.

In addition, you want to ensure that you run relatively large batches in each task (> 100 products). There is a startup cost for each instance of the valdidator (several seconds in my experience), so that should be distributed over a large number of products to reduce the impact.


### What can parallel validation speed up?

Parallel validation will speed up individual product validtions, such as label and data content validations. These tasks can be completed independently of all other validation tasks, and can be distributed over many instances.

### What can't parallel validation speed up?

Parallel validation will not speed up referential integrity validation. The entire bundle/collection has to be considered when running in parallel, so this must be run as a single process. In the future, it may be possible to persist the information needed to perform referential integrity validation (in a datastore such as the registry), but that is not the case at this time.

## How to use the parallel validator script

```bash
cd /path/to/parallel_validation
./validate_parallel.sh validation_directory config_file catalog_file report_directory [workers] [batch_size]
```

If you need to ignore superseded files, you can run this variant of the script:

```bash
cd /path/to/parallel_validation
./validate_parallel_no_superseded.sh validation_directory config_file catalog_file report_directory [workers] [batch_size]
```

Options:
* validation directory - this where all of the files that you want to validate are stored. It doesn't matter if this is a bundle, collection, or even a subset of a collection.
* config file - this is where you will specify options for the validate command, instead of on the command line. This makes the configurations reusable, and also simplifies the script.
* catalog file - this will redirect all of the requests for schema and schematron files to another location, preferably on your local filesystem. It is important to have one of these, since the validator will reach out to the internet to reload the catalogs on a regular basis otherwise, degrading performance.
* report directory - this is where all of the output files are stored. This directory will be automatically created if if does not exist.
* workers - this specifies how many instances of validate you want to run at once. If you don't provide this, the script will default to 4. See below to get the correct value.
* batch size - this specifies how many products each validate instance will process. If you don't providde this, the script will default to 1000. This should probably be left as-is. Going higher will likely exceed the maximum argument list length, and will get clamped back down anyway.

### How many processes do I need?

Generally, you can support as many processes as you have CPU cores. There is a good chance that each validator instance will utilize the entire core, so there is generally no need to
run with more cores. In fact, if the validator does not use the entire core, there is a good chance that you are I/O bound at this point, and can probably reduce the number of cores that you are using.

You may also want to leave one core free so that the OS can use it for other tasks. The OS should actually schedule things so that this is not a problem, but I like to
leave one free anyway.

### Why are there so many files?

Each validation run produces its own independent output file. This is necessary, since multiple processes writing to the same file with no coordination will produce an unusable output.

## How to interpret the results

### Combining overall statistics

`processing_totals.sh (report_dir)/*`

### Combining message statistics

`message_totals.sh (report_dir)/*`

### Combining product-level messages

`product_results.sh (report_dir)/*`

