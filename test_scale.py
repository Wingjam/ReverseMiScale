from scale import Scale

class TestScale(object):

    def test_scale_are_equals(self):
        # Arrange
        first_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            isStabilized=False,
            loadRemoved=True,
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("820000e2070b0f082924"),
            sequence= 10532,
            unit= "kg",
            weight= 0.0
        )
        second_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            isStabilized=False,
            loadRemoved=True,
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("820000e2070b0f082924"),
            sequence= 10532,
            unit= "kg",
            weight= 0.0
        )

        # Act, Assert
        assert first_scale == second_scale
