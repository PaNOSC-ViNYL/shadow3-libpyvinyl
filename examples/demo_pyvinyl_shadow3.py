

from shadow3libpyvinyl.Shadow3Calculator import Shadow3Calculator


if True:
    calculator  = Shadow3Calculator("")

    calculator.setParams(number_of_optical_elements=1)


    calculator.parameters["oe0.FDISTR"]       = 3
    calculator.parameters["oe0.F_COLOR"]      = 3
    calculator.parameters["oe0.F_PHOT"]       = 0
    calculator.parameters["oe0.HDIV1"]        = 0.0
    calculator.parameters["oe0.HDIV2"]        = 0.0
    calculator.parameters["oe0.NPOINT"]       = 10000
    calculator.parameters["oe0.PH1"]          = 8799.999
    calculator.parameters["oe0.PH2"]          = 8799.999
    calculator.parameters["oe0.SIGDIX"]       = 4.728541797631135e-06
    calculator.parameters["oe0.SIGDIZ"]       = 4.095010077148124e-06
    calculator.parameters["oe0.SIGMAX"]       = 0.0015810951361940363
    calculator.parameters["oe0.SIGMAZ"]       = 0.0006681031579752021
    calculator.parameters["oe0.VDIV1"]        = 0.0
    calculator.parameters["oe0.VDIV2"]        = 0.0
    calculator.parameters["oe1.DUMMY"]        = 1.0
    calculator.parameters["oe1.FMIRR"]        = 3
    calculator.parameters["oe1.FWRITE"]       = 1
    calculator.parameters["oe1.T_IMAGE"]      = 1000.0
    calculator.parameters["oe1.T_INCIDENCE"]  = 89.828
    calculator.parameters["oe1.T_REFLECTION"] = 89.828
    calculator.parameters["oe1.T_SOURCE"]     = 4000.0


    ### Run the backengine
    calculator.backengine(write_start_files_root="start")


    #
    # make plot
    #
    import Shadow
    try:
        from srxraylib.plot.gol import set_qt
        set_qt()
    except:
        pass

    Shadow.ShadowTools.plotxy(calculator.data, 1, 3, nbins=101, nolost=1, title="Real space")


    #
    # save files
    calculator.saveH5("tmp.h5")
    calculator.parameters.to_json("my_parameters.json")
    print(calculator.parameters)

#
# retrieve from json
#
if True:

    new_calculator = Shadow3Calculator("from file")
    new_calculator.setParams(number_of_optical_elements=1, json="my_parameters.json")

    new_calculator.backengine(write_start_files_root="start_new")
    #
    # new_calculator.saveH5("tmp.h5")
    #
    import Shadow
    Shadow.ShadowTools.plotxy(new_calculator.data, 1, 3, nbins=101, nolost=1, title="Real space")


