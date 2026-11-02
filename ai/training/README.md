# Model Training Workflow

This folder documents the training workflow; it does not contain trained weights.

## Vehicle detector

1. Prepare licensed vehicle images and YOLO-format bounding-box labels as described in [../dataset/README.md](../dataset/README.md).
2. Create a dataset YAML file with absolute or correctly resolved paths and a stable class order. Start from [../configs/vehicle_dataset.yaml.example](../configs/vehicle_dataset.yaml.example).
3. Install the backend requirements in an isolated Python environment.
4. Run a baseline training experiment, for example:

```bash
yolo detect train model=yolo11n.pt data=/absolute/path/to/data.yaml epochs=50 imgsz=640 batch=8 seed=42
```

Choose a model/checkpoint compatible with the installed Ultralytics version and document its license and source. The example is a starting point, not a prescribed optimal configuration.

## Accident-event model

Vehicle bounding-box training is not accident-event training. An accident-event classifier requires temporally labeled video clips or sequences, a documented event definition, and video-level train/validation/test splits. The existing heuristic AccidentAnalyzer remains a baseline until such a model is implemented and evaluated.

## Experiment record

For every run, record:
- dataset version and split-manifest hash;
- model architecture and pretrained checkpoint source;
- hyperparameters, seed, software versions and hardware;
- training duration and selected checkpoint;
- validation selection rule and final test metrics;
- failure cases, class imbalance and limitations.

Do not tune against the final test split. Store large weights and raw datasets outside Git unless repository policy and dataset licensing explicitly allow them.
