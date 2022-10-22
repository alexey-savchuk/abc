from model.bid import Bid


class StepRecorder:

    pushed: Bid = None
    poped: Bid = None
    refused: Bid = None
