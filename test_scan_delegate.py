from scale import Scale
from miScale import ScanDelegate

class TestHandleData(object):


    def test_data_not_stabilized_load_removed(self):
        # Arrange
        input_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("820000e2070b0f082924"),
        )
        expected_scale = Scale(
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

        # Act
        def callback(result_scale):
            # Assert
            assert expected_scale == result_scale
        
        delegate = ScanDelegate("c8:0f:10:bf:cc:66", callback, False)
        delegate.handleData(input_scale)


    def test_data_stabilized_load_not_removed(self):
        # Arrange
        input_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("226455e2070b0f0c1d1b"),
        )
        expected_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            isStabilized=True,
            loadRemoved=False,
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("226455e2070b0f0c1d1b"),
            sequence= 7451,
            unit= "kg",
            weight= 109.3
        )

        # Act
        def callback(result_scale):
            # Assert
            assert expected_scale == result_scale
        
        delegate = ScanDelegate("c8:0f:10:bf:cc:66", callback, False)
        delegate.handleData(input_scale)


    def test_data_stabilized_load_removed(self):
        # Arrange
        input_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("a26455e2070b0f082a23"),
        )
        expected_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            isStabilized=True,
            loadRemoved=True,
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("a26455e2070b0f082a23"),
            sequence= 10787,
            unit= "kg",
            weight= 109.3
        )

        # Act
        def callback(result_scale):
            # Assert
            assert expected_scale == result_scale
        
        delegate = ScanDelegate("c8:0f:10:bf:cc:66", callback, False)
        delegate.handleData(input_scale)


    def test_data_not_stabilized_load_not_removed(self):
        # Arrange
        input_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("02e402b2080101010422"),
        )
        expected_scale = Scale(
            UUID="181d",
            address="c8:0f:10:bf:cc:66",
            isStabilized=False,
            loadRemoved=False,
            manufacturerData= bytes.fromhex("5701c80f10bfcc66"),
            rawData= bytes.fromhex("02e402b2080101010422"),
            sequence= 1058,
            unit= "kg",
            weight= 3.7
        )

        # Act
        def callback(result_scale):
            # Assert
            assert expected_scale == result_scale
        
        delegate = ScanDelegate("c8:0f:10:bf:cc:66", callback, False)
        delegate.handleData(input_scale)
