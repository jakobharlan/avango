# -*- Mode:Python -*-

##########################################################################
#                                                                        #
# This file is part of AVANGO.                                           #
#                                                                        #
# Copyright 1997 - 2009 Fraunhofer-Gesellschaft zur Foerderung der       #
# angewandten Forschung (FhG), Munich, Germany.                          #
#                                                                        #
# AVANGO is free software: you can redistribute it and/or modify         #
# it under the terms of the GNU Lesser General Public License as         #
# published by the Free Software Foundation, version 3.                  #
#                                                                        #
# AVANGO is distributed in the hope that it will be useful,              #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU Lesser General Public       #
# License along with AVANGO. If not, see <http://www.gnu.org/licenses/>. #
#                                                                        #
##########################################################################

import avango.display

class AutoStereoDisplay(avango.display.Display):

    def __init__(self, inspector, options):
        super(AutoStereoDisplay, self).__init__("AutoStereoDisplay", inspector)

        window = self.make_window(0, 0, 1200, 1600, 0.33, 0.43, True)
        window.Name.value = ""
        self.add_window(window, avango.osg.make_trans_mat(0, 1.7, -0.7), 0)

        user = avango.display.nodes.User()
        user.Matrix.value = avango.osg.make_trans_mat(avango.osg.Vec3(0., 1.7, 0.))
        self.add_user(user)
