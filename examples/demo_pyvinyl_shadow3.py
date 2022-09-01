

from shadow3libpyvinyl.Shadow3Calculator import Shadow3Calculator
from libpyvinyl.Parameters.Collections import CalculatorParameters
from libpyvinyl.Parameters.Parameter import Parameter

########################################################################################################################
#
# auxiliary functions
#

def get_calculator_parameters(source=True,oe=True):

    parameters = CalculatorParameters()

    if source:
        p = Parameter("oe0.FDISTR"      , "" )  ; p.value   = 3                        ; parameters.add(p)
        p = Parameter("oe0.F_COLOR"     , "" )  ; p.value   = 3                        ; parameters.add(p)
        p = Parameter("oe0.F_PHOT"      , "" )  ; p.value   = 0                        ; parameters.add(p)
        p = Parameter("oe0.HDIV1"       , "" )  ; p.value   = 0.0                      ; parameters.add(p)
        p = Parameter("oe0.HDIV2"       , "" )  ; p.value   = 0.0                      ; parameters.add(p)
        p = Parameter("oe0.NPOINT"      , "" )  ; p.value   = 10000                    ; parameters.add(p)
        p = Parameter("oe0.PH1"         , "" )  ; p.value   = 8799.999                 ; parameters.add(p)
        p = Parameter("oe0.PH2"         , "" )  ; p.value   = 8799.999                 ; parameters.add(p)
        p = Parameter("oe0.SIGDIX"      , "" )  ; p.value   = 4.728541797631135e-06    ; parameters.add(p)
        p = Parameter("oe0.SIGDIZ"      , "" )  ; p.value   = 4.095010077148124e-06    ; parameters.add(p)
        p = Parameter("oe0.SIGMAX"      , "" )  ; p.value   = 0.0015810951361940363    ; parameters.add(p)
        p = Parameter("oe0.SIGMAZ"      , "" )  ; p.value   = 0.0006681031579752021    ; parameters.add(p)
        p = Parameter("oe0.VDIV1"       , "" )  ; p.value   = 0.0                      ; parameters.add(p)
        p = Parameter("oe0.VDIV2"       , "" )  ; p.value   = 0.0                      ; parameters.add(p)

    if oe:
        p = Parameter("oe1.DUMMY"       , "" )  ; p.value   = 1.0                      ; parameters.add(p)
        p = Parameter("oe1.FMIRR"       , "" )  ; p.value   = 3                        ; parameters.add(p)
        p = Parameter("oe1.FWRITE"      , "" )  ; p.value   = 1                        ; parameters.add(p)
        p = Parameter("oe1.T_IMAGE"     , "" )  ; p.value   = 1000.0                   ; parameters.add(p)
        p = Parameter("oe1.T_INCIDENCE" , "" )  ; p.value   = 89.828                   ; parameters.add(p)
        p = Parameter("oe1.T_REFLECTION", "" )  ; p.value   = 89.828                   ; parameters.add(p)
        p = Parameter("oe1.T_SOURCE"    , "" )  ; p.value   = 4000.0                   ; parameters.add(p)

    return parameters

def do_plotxy_plot(calculator, title=""):
    import Shadow
    try:
        from srxraylib.plot.gol import set_qt
        set_qt()
    except:
        pass

    beam = Shadow.Beam(N=calculator.data.get_data()["nrays"])
    beam.rays = calculator.data.get_data()["rays"]
    Shadow.ShadowTools.plotxy(beam, 1, 3, nbins=101, nolost=1, title=title+" Real space")


########################################################################################################################


#
# start-to-end calculation (and write json file with parameters)
#
if True:
    calculator = Shadow3Calculator("test", None, parameters=get_calculator_parameters())
    calculator.backengine()


    do_plotxy_plot(calculator, title="FULL SIMULATION. ")

    #
    # save parameters
    calculator.parameters.to_json("my_parameters.json")
    print("calculator parameters saved to file: my_parameters.json")
    # print(calculator.parameters)


#
# calculation retrieving parameters from json file previously created
#
if True:

    params_json = CalculatorParameters.from_json("my_parameters.json")
    new_calculator = Shadow3Calculator("from file", None, parameters=params_json)
    new_calculator.backengine()

    # plot
    do_plotxy_plot(new_calculator, title="PARAMETERS FROM JSON FILE. ")


#
# calculation in two steps:
#     1) calculate only sources and save to file
#     2) trace optical element reading source from the file

if True:

    from shadow3libpyvinyl.Shadow3Data import Shadow3Data, Shadow3BeamFormat, Shadow3OpenPMDFormat

    calculator = Shadow3Calculator("test", None, parameters=get_calculator_parameters(source=True,oe=False))
    calculator.backengine()
    # calculator.data.write("tmp11.dat", Shadow3BeamFormat)    # raw data format
    calculator.data.write("tmp11.h5", Shadow3OpenPMDFormat)  # openPMD data format

    # load input data
    input_data = Shadow3Data("")
    # input_data.set_file("tmp11.dat", Shadow3BeamFormat)   # raw data format
    input_data.set_file("tmp11.h5", Shadow3OpenPMDFormat)  # openPMD data format

    # trace oe with saved source
    new_calculator = Shadow3Calculator("source from file", input_data, parameters=get_calculator_parameters(source=False,oe=True))
    new_calculator.backengine()

    #
    # plot
    #
    do_plotxy_plot(new_calculator, title="SOURCE FROM FILE. ")
