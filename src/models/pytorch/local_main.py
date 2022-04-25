import os
from packaging import version
from optuna.integration import PyTorchLightningPruningCallback
import optuna
from pytorch_lightning import Trainer
import pytorch_lightning as pl
import torch
from src.models.pytorch.TweetLitModule import TweetLitModule
from src.data.load_dataset.TwitterDataModule import TwitterDataModule


def objective(trial: optuna.trial.Trial) -> float:

    PERCENT_VALID_EXAMPLES = 0.1
    CLASSES = 3
    EPOCHS = 3

    # We optimize the number of layers, hidden units in each layer and dropouts.
    n_layers = trial.suggest_int("n_layers", 1, 3)
    weight_decay = trial.suggest_float("weight_decay", 0.5, 1)
    dropout = trial.suggest_float("dropout", 0, 0.5)
    learning_rate = trial.suggest_loguniform("learning_rate", 1e-6, 5e-1)
    output_dims = [
        trial.suggest_int("n_units_l{}".format(i), 4, 128, log=True) for i in range(n_layers)
    ]
    output_dims.append(CLASSES)

    hparams_ = {
        'weight_decay': weight_decay,
        'lr': learning_rate,
        'embed_dim': 384,
        'dropout': dropout,
        'num_label': 3,
        'output_dims': 	output_dims,
    }
    model = TweetLitModule(hparams_)

    csv_test = "src/tests/test_set_240tweets_labeled_0410.csv"
    csv_train = "data/processed/allocine/allocine_trainset_160000reviews.csv"
    # args.in_csv
    dm = TwitterDataModule(csv_test_path=csv_test,
                           csv_train_path=csv_train)

    trainer = pl.Trainer(
        logger=True,
        limit_val_batches=PERCENT_VALID_EXAMPLES,
        checkpoint_callback=False,
        max_epochs=EPOCHS,
        gpus=1 if torch.cuda.is_available() else None,
        callbacks=[PyTorchLightningPruningCallback(trial, monitor="val/acc")],
    )

    trainer.logger.log_hyperparams(hparams_)

    trainer.fit(model, datamodule=dm)
    # _ = trainer.test(model, datamodule=dm)

    print(f"{trainer.callback_metrics = }")
    # print(f"{trainer.callback_metrics.items() = }")

    return trainer.callback_metrics["val/acc"].item()


def torch_hp_search():
    pruner: optuna.pruners.BasePruner = (
        optuna.pruners.MedianPruner()
    )

    study = optuna.create_study(direction="maximize", pruner=pruner)
    study.optimize(objective, n_trials=None, timeout=None)

    print("Number of finished trials: {}".format(len(study.trials)))

    print("Best trial:")
    trial = study.best_trial

    print("  Value: {}".format(trial.value))

    print("  Params: ")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))


def torch_main(args):
    search_hyper_params = True
    if search_hyper_params:
        torch_hp_search()
    else:
        trainer = Trainer(max_epochs=3, accelerator='gpu', devices=1)

        csv_test = "src/tests/test_set_240tweets_labeled_0410.csv"
        csv_train = "data/processed/allocine/allocine_trainset_160000reviews.csv"
        dm = TwitterDataModule(csv_test_path=csv_test,
                               csv_train_path=csv_train)

        load_model = False
        if load_model:
            mdl_weights = "lightning_logs/version_6/checkpoints/epoch=9-step=160000.ckpt"
            hparams_file = "lightning_logs/version_6/hparams.yaml"
            model = TweetLitModule.load_from_checkpoint(
                checkpoint_path=mdl_weights, hparams_file=hparams_file)
        else:
            model = TweetLitModule()

        trainer.fit(model=model, datamodule=dm)
        _ = trainer.test(model, datamodule=dm)
