import avango
import avango.script
from avango.script import field_has_changed
import avango.gua
import avango.oculus
from examples_common.GuaVE import GuaVE


class TimedRotate(avango.script.Script):
    TimeIn = avango.SFFloat()
    MatrixOut = avango.gua.SFMatrix4()

    def evaluate(self):
        self.MatrixOut.value = avango.gua.make_rot_mat(
            self.TimeIn.value * 2.0, 0.0, 1.0, 0.0)


def start():
    # setup scenegraph
    graph = avango.gua.nodes.SceneGraph(Name="scenegraph")
    loader = avango.gua.nodes.TriMeshLoader()

    monkey1 = loader.create_geometry_from_file(
        "monkey",
        "data/objects/monkey.obj",
        avango.gua.LoaderFlags.NORMALIZE_SCALE)

    monkey2 = loader.create_geometry_from_file(
        "monkey",
        "data/objects/monkey.obj",
        avango.gua.LoaderFlags.NORMALIZE_SCALE)

    monkey1.Material.value.set_uniform(
        "Color",
        avango.gua.Vec4(1.0, 0.766, 0.336, 1.0))
    monkey1.Material.value.set_uniform("Roughness", 0.3)
    monkey1.Material.value.set_uniform("Metalness", 1.0)

    monkey2.Material.value.set_uniform(
        "Color", avango.gua.Vec4(1.0, 0.266, 0.136, 1.0))
    monkey2.Material.value.set_uniform("Roughness", 0.6)
    monkey2.Material.value.set_uniform("Metalness", 0.0)

    transform1 = avango.gua.nodes.TransformNode(
        Children=[monkey1]
        )
    transform2 = avango.gua.nodes.TransformNode(
        Transform=avango.gua.make_trans_mat(-0.5, 0.0, 0.0),
        Children=[monkey2]
        )

    light = avango.gua.nodes.LightNode(
        Type=avango.gua.LightType.POINT,
        Name="light",
        Color=avango.gua.Color(1.0, 1.0, 1.0),
        Brightness=100.0,
        Transform=(avango.gua.make_trans_mat(1, 1, 5) *
                   avango.gua.make_scale_mat(30, 30, 30))
        )
    
    window = avango.oculus.nodes.OculusWindow()

    #notice, that the oculus screen transforms and translations are automatically
    #computed by the oculus. do not try to enter them yourself, or you will
    #most likely get a wrong result due to influence of the lenses

    #accessible fields:
    #    SensorOrientation ##head pose (rotation and translation)
    #    Resolution ##window resolution
    #    EyeResolution ##recommended eye resolution (behaves strange so far)
    #    LeftScreenSize  ## size of left screen in meters
    #    RightScreenSize ## size of right screen in meters
    #    LeftScreenTranslation  ## translation of left screen in meters
    #    RightScreenTranslation ## translation of right screen in meters 
    #    EyeDistance ## distance between both eyes in meters. for SDKs < v0.6, this is fixed to 0.064

    # start the window in fullscreen and with the oculus window as primary display in order to fit the
    # window nicely on the HMD
    
    window.Size.value = window.Resolution.value
    window.LeftResolution.value = window.Resolution.value
    window.RightResolution.value = window.Resolution.value
    window.EnableFullscreen.value = True

    
    avango.gua.register_window("window", window)

    cam = avango.gua.nodes.CameraNode(
        LeftScreenPath="/nav/head/left_screen",
        RightScreenPath="/nav/head/right_screen",
        SceneGraph="scenegraph",
        Resolution=window.LeftResolution.value,
        OutputWindowName="window",
        EyeDistance=window.EyeDistance.value,
        EnableStereo=True
        )

    res_pass = avango.gua.nodes.ResolvePassDescription()
    res_pass.EnableSSAO.value = True
    res_pass.SSAOIntensity.value = 4.0
    res_pass.SSAOFalloff.value = 10.0
    res_pass.SSAORadius.value = 7.0

    #res_pass.EnableScreenSpaceShadow.value = True

    res_pass.EnvironmentLightingColor.value = avango.gua.Color(0.1, 0.1, 0.1)
    res_pass.ToneMappingMode.value = avango.gua.ToneMappingMode.UNCHARTED
    res_pass.Exposure.value = 1.0
    res_pass.BackgroundColor.value = avango.gua.Color(0.45, 0.5, 0.6)

    anti_aliasing = avango.gua.nodes.SSAAPassDescription()

    pipeline_description = avango.gua.nodes.PipelineDescription(
        Passes=[
            avango.gua.nodes.TriMeshPassDescription(),
            avango.gua.nodes.LightVisibilityPassDescription(),
            res_pass,
            anti_aliasing,
            ])

    cam.PipelineDescription.value = pipeline_description


    left_screen = avango.gua.nodes.ScreenNode(
        Name="left_screen",
        Width=window.LeftScreenSize.value.x,
        Height=window.LeftScreenSize.value.y,
        Transform=avango.gua.make_trans_mat(
            window.LeftScreenTranslation.value
            )
        )

    right_screen = avango.gua.nodes.ScreenNode(
        Name="right_screen",
        Width=window.RightScreenSize.value.x,
        Height=window.RightScreenSize.value.y,
        Transform=avango.gua.make_trans_mat(
            window.RightScreenTranslation.value
            )
        )

    head = avango.gua.nodes.TransformNode(
        Name="head",
        Children=[left_screen, right_screen, cam],
        Transform=avango.gua.make_identity_mat()
        )

    nav = avango.gua.nodes.TransformNode(
        Name="nav",
        Transform=avango.gua.make_trans_mat(0.0, 0.0, 2.0),
        Children=[head]
        )

    graph.Root.value.Children.value = [transform1, transform2, light, nav]

    #setup viewer
    viewer = avango.gua.nodes.Viewer()
    viewer.SceneGraphs.value = [graph]
    viewer.Windows.value = [window]

    monkey_updater = TimedRotate()

    timer = avango.nodes.TimeSensor()
    monkey_updater.TimeIn.connect_from(timer.Time)

    head.Transform.connect_from(window.SensorOrientation)
    transform1.Transform.connect_from(monkey_updater.MatrixOut)

    guaVE = GuaVE()
    guaVE.start(locals(), globals())

    viewer.run()


if __name__ == '__main__':
  start()

