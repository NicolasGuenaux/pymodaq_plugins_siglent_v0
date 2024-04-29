from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter
from siglent_wrapper import ActuatorWrapper

#     #  TODO Replace this fake class with the import of the real python wrapper of your instrument
#     pass
## No python wrapper for Siglent SDG products (no dll files, only SCPI commands).

# TODO:
# (1) change the name of the following class to DAQ_Move_TheNameOfYourChoice
# (2) change the name of this file to daq_move_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_move_plugins
class DAQ_Move_Siglent(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    # TODO Complete the docstring of your plugin with:
    #     * The set of controllers and actuators that should be compatible with this instrument plugin.
    #     * With which instrument and controller it has been tested.
    #     * The version of PyMoDAQ during the test.
    #     * The version of the operating system.
    #     * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    
    # TODO add your particular attributes here if any

    """
    _controller_units = ActuatorWrapper.units  # TODO for your plugin: put the correct unit here
    is_multiaxes = True  # TODO for your plugin set to True if this plugin is controlled for a multiaxis controller
    _axis_names = ['Amplitude', 'Phase']  # TODO for your plugin: complete the list
    _epsilon = 0.1  # TODO replace this by a value that is correct depending on your controller
    data_actuator_type = DataActuatorType['DataActuator']  # wether you use the new data style for actuator otherwise set this
    # as  DataActuatorType['float']  (or entirely remove the line)

    params = [  
        {'title': 'Frequency:', 'name': 'frequency', 'type': 'float', 'value': 10000000},
        {'title': 'Offset:', 'name': 'offset', 'type': 'float', 'value': 0},
        {'title': 'Delay:', 'name': 'delay', 'type': 'float', 'value': 0.000005},
        {'title': 'Rep number:', 'name': 'cycles', 'type': 'int', 'value': 1},
        {'title': 'Wavetype:', 'name': 'wavetype', 'type': 'text', 'value': "SINE"},
        {'title': 'File:', 'name': 'file', 'type': 'text', 'value': ""},
         # TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
                ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)
    # _epsilon is the initial default value for the epsilon parameter allowing pymodaq to know if the controller reached
    # the target value. It is the developer responsibility to put here a meaningful value


    def ini_attributes(self):
        # #  TODO declare the type of the wrapper (and assign it to self.controller) you're going to use for easy
        # #  autocompletion
        self.controller: ActuatorWrapper = None

        # Not sure if it is necessary to init them at this point
        # These are the initial values when the instrument is turned on



        #TODO declare here attributes you want/need to init with a default value
        pass




    def get_actuator_value(self): 
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        pos = DataActuator(data=self.controller.get_pos())  # when writing your own plugin replace this line
        pos = self.get_position_with_scaling(pos)
        return pos

    def close(self):
        """Terminate the communication protocol"""
        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        #  self.controller.your_method_to_terminate_the_communication()  # when writing your own plugin replace this line

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        ## TODO for your custom plugin
        if param.name() == "axis":
            self.controller.set_axis(self.axis_name)
        elif param.name() == "frequency":
            self.controller.set_frequency(param.value())
        elif param.name() == "offset":
            self.controller.set_offset(param.value())
        elif param.name() == "delay":
            self.controller.set_delay(param.value())
        elif param.name() == "cycles":
            self.controller.set_cycles(param.value())
        elif param.name() == "wavetype":
            self.controller.set_wavetype(param.value())
        elif param.name() == "file":
            self.controller.set_arbwave(param.value())
        else:
            pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        # raise NotImplemented  # TODO when writing your own plugin remove this line and modify the one below
        self.controller = self.ini_stage_init(old_controller=controller,
                                              new_controller=ActuatorWrapper())
        self.controller.open_communication()

        self.controller.__init__()  # todo
        info = "Typical CH1 settings turned on"
        initialized = self.controller.open_communication()

        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_pos(value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['position updated']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_rel_pos(value.value())  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['position updated']))

    def move_home(self):
        """Call the reference method of the controller"""

        ## TODO for your custom plugin
        # raise NotImplemented  # when writing your own plugin remove this line
        self.controller.set_amplitude(amp=2)  # when writing your own plugin replace this line
        self.controller.set_phase(phi=0)
        self.emit_status(ThreadCommand('Update_Status', ['moved home (amp = 2, phi=0)']))

    def stop_motion(self):
      """Stop the actuator and emits move_done signal"""

      ## TODO for your custom plugin
    #   raise NotImplemented  # when writing your own plugin remove this line
      self.controller.set_state("OFF")  # when writing your own plugin replace this line
      self.emit_status(ThreadCommand('Update_Status', ['channel output OFF']))


if __name__ == '__main__':
    main(__file__)
