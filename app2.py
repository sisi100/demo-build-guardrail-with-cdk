import aws_cdk as cdk
import jsii
from aws_cdk import aws_lambda
from constructs import IConstruct


# --------------------------------------
# ガードレール的なモノを定義する
@jsii.implements(cdk.IAspect)
class HogeAspect:
    def visit(self, node: IConstruct):
        if isinstance(node, aws_lambda.Function):
            cfn_node: aws_lambda.CfnFunction = node.node.default_child
            # アーキテクチャーの判断
            if not cfn_node.architectures == ["arm64"]:
                cdk.Annotations.of(node).add_error("ARM64のが安いよ")
            # メモリーの判断
            if not cfn_node.memory_size:
                cdk.Annotations.of(node).add_error("メモリーチューニングしよう")

    def error(self, node, message):
        cdk.Annotations.of(node).add_error(message)


# --------------------------------------
# CDKでアプリを作る
app = cdk.App()
stack = cdk.Stack(app, "test")

lambda_ = aws_lambda.Function(
    stack,
    "function",
    code=aws_lambda.Code.from_asset("runtime"),
    runtime=aws_lambda.Runtime.PYTHON_3_9,
    handler="index.handler",
    architecture=aws_lambda.Architecture.ARM_64,
    memory_size=256,
)

cdk.Aspects.of(stack).add(HogeAspect())

app.synth()