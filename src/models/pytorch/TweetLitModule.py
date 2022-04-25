from typing import Any, List
import torch
from pytorch_lightning import LightningModule
from torchmetrics import MaxMetric
from torchmetrics.classification.accuracy import Accuracy
from sentence_transformers import SentenceTransformer

from torch import nn


class TweetLitModule(LightningModule):
    """Example of LightningModule for MNIST classification.
    A LightningModule organizes your PyTorch code into 5 sections:
                                    - Computations (init).
                                    - Train loop (training_step)
                                    - Validation loop (validation_step)
                                    - Test loop (test_step)
                                    - Optimizers (configure_optimizers)
    Read the docs:
                                    https://pytorch-lightning.readthedocs.io/en/latest/common/lightning_module.html
    """

    def __init__(self, hparams_):
        super().__init__()

        # loss function
        self.criterion = torch.nn.CrossEntropyLoss()
        # self.criterion = nn.MSELoss()

        self.hparams_ = hparams_
        # {
        # 	'weight_decay': 0.999,
        # 	'lr': 1e-1,
        # 	'embed_dim': 384,
        # 	'num_label': 3,
        # 	'output_dims': [128, 64, 32, 3],
        # }

        # use separate metric instance for train, val and test step
        # to ensure a proper reduction over the epoch
        self.train_acc = Accuracy()
        self.val_acc = Accuracy()
        self.test_acc = Accuracy()
        # self.fn_acc = lambda x, y: 42
        # Accuracy()
        self.val_acc_best = MaxMetric()
        self._build_model()

    def _build_model(self):
        self.sentence_embed = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        auto_model = self.sentence_embed._first_module().auto_model
        for param in auto_model.parameters():
            param.requires_grad = False

        # self.sentence_embed.freeze()
        # self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=True)
        dropout = 0.2
        layers: List[nn.Module] = []

        input_dim: int = self.hparams_['embed_dim']
        for output_dim in self.hparams_['output_dims']:
            layers.append(nn.Linear(input_dim, output_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(self.hparams_['dropout']))
            input_dim = output_dim

        self.fc_layers: nn.Module = nn.Sequential(*layers)

        self.softmax = nn.Softmax(dim=1)
        # self.init_weights()

    # def forward(self, text, offsets):
    def forward(self, text):
        # print(f"{text = }")
        # print(f"{type(text) = }")
        # print(f"{text.shape = }")
        # print(f"{text.dtype = }")
        # embedded = self.embedding(text, offsets)
        embedded = self.sentence_embed.encode(list(text))
        # print(f"{embedded.shape = }")
        t_embedded = torch.from_numpy(embedded).to(self.device)
        out = self.fc_layers(t_embedded)
        # print(f"{out.shape = }")
        return self.softmax(out)

    def step(self, batch: Any):
        x, y = batch
        logits = self.forward(x)

        logits = logits.to(torch.float)
        y = y.to(torch.float)
        loss = self.criterion(logits, y)
        y = y.to(torch.int)

        return loss, logits, y

    def training_step(self, batch: Any, batch_idx: int):
        loss, preds, targets = self.step(batch)

        # log train metrics
        acc = self.train_acc(preds, targets)
        self.log("train/loss", loss, on_step=False,
                 on_epoch=True, prog_bar=False)
        self.log("train/acc", acc, on_step=False, on_epoch=True, prog_bar=True)

        # we can return here dict with any tensors
        # and then read it in some callback or in `training_epoch_end()`` below
        # remember to always return loss from `training_step()` or else backpropagation will fail!
        return {"loss": loss, "preds": preds, "targets": targets}

    def validation_step(self, batch: Any, batch_idx: int):
        self.eval()
        with torch.no_grad():
            loss, preds, targets = self.step(batch)
        self.train()

        # log val metrics
        # print(f"{preds.shape = }")
        # print(f"{targets.shape = }")
        acc = self.val_acc(preds, targets)
        # print(f"{acc.shape = }")
        self.log("val/loss", loss, on_step=False,
                 on_epoch=True, prog_bar=False)
        self.log("val/acc", acc, on_step=False, on_epoch=True, prog_bar=True)
        self.log("val_acc", acc)

        return {"loss": loss, "preds": preds, "targets": targets}

    def validation_epoch_end(self, outputs: List[Any]):
        acc = self.val_acc.compute()  # get val accuracy from current epoch
        self.val_acc_best.update(acc)
        self.log("val/acc_best", self.val_acc_best.compute(),
                 on_epoch=True, prog_bar=True)

    def test_step(self, batch: Any, batch_idx: int):
        self.eval()
        with torch.no_grad():
            loss, preds, targets = self.step(batch)
        self.train()

        # log test metrics
        acc = self.test_acc(preds, targets)
        self.log("test/loss", loss, on_step=False, on_epoch=True)
        self.log("test/acc", acc, on_step=False, on_epoch=True)

        return {"loss": loss, "preds": preds, "targets": targets}

    def on_train_epoch_end(self):
        # reset metrics at the end of every epoch
        self.train_acc.reset()

    def on_test_epoch_end(self):
        self.test_acc.reset()

    def on_validation_epoch_end(self):
        self.val_acc.reset()

    def configure_optimizers(self):
        """Choose what optimizers and learning-rate schedulers to use in your optimization.
        Normally you'd need one. But in the case of GANs or similar you might have multiple.
        See examples here:
                                        https://pytorch-lightning.readthedocs.io/en/latest/common/lightning_module.html#configure-optimizers
        """
        return torch.optim.Adam(
            params=self.parameters(), lr=self.hparams_['lr'], weight_decay=self.hparams_['weight_decay']
        )
