from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import ValidationError, DataRequired

from app.models import Tank


class BiosConfigForm(FlaskForm):
    Share_NIC_Control_output = RadioField('Share NIC Control output',
                                          choices=[(-1, 'No Change'), ("00", 'OCP NIC'), ("01", 'PCH NIC')],
                                          default=-1)

    Wake_on_LAN_Control = RadioField('Wake on LAN Control',
                                     choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                     default=-1)

    Security_Device_Support = RadioField('Security Device Support',
                                         choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                         default=-1)

    Console_Redirection = RadioField('Console Redirection',
                                     choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                     default=-1)

    Above_4G_Decoding = RadioField('Above 4G Decoding',
                                   choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                   default=-1)

    SR_IOV_Support = RadioField('SR-IOV Support',
                                choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                default=-1)

    Network_Stack = RadioField('Network Stack',
                               choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                               default=-1)

    Ipv4_PXE_Support = RadioField('Ipv4 PXE Support',
                                  choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                  default=-1)

    Ipv6_PXE_Support = RadioField('Ipv6 PXE Support',
                                  choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                  default=-1)

    Intel_HT_Technology = RadioField('Intel HT Technology',
                                     choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                     default=-1)

    Intel_TXT = RadioField('Intel TXT',
                           choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                           default=-1)

    Intel_VT = RadioField('Intel VT',
                          choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                          default=-1)

    Hardware_Prefetcher = RadioField('Hardware Prefetcher',
                                     choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                     default=-1)

    NUMA_Optimized = RadioField('NUMA Optimized',
                                choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                default=-1)

    Enforce_POR = RadioField('Enforce POR',
                             choices=[(-1, 'No Change'), ("03", 'Auto'), ("02", 'Disable'), ("00", "POR")],
                             default=-1)

    Patrol_Scrub = RadioField('Patrol Scrub',
                              choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                              default=-1)

    Intel_VT_for_Directed_IO_VT_d = RadioField('Intel VT for Directed I/O (VT-d)',
                                               choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                               default=-1)

    Enhanced_Intel_Speedstep_Technology = RadioField('Enhanced Intel Speedstep Technology',
                                                     choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                                     default=-1)

    Intel_Turbo_Boost_Technology = RadioField('Intel Turbo Boost Technology',
                                              choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                              default=-1)

    Hardware_P_State = RadioField('Hardware P-State',
                                  choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                  default=-1)

    CPU_C6_Report = RadioField('CPU C6 Report',
                               choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable'), ("FF", "AUTO")],
                               default=-1)

    Enhanced_Halt_State_C1E = RadioField('Enhanced Halt State (C1E)',
                                         choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                         default=-1)

    Power_Performance_Turing = RadioField('Power Performance Turing',
                                          choices=[(-1, 'No Change'), ("01", 'BIOS controls EPB'), ("00", 'OS Controls EPB')],
                                          default=-1)

    PECI_PCS_EPB = RadioField('PECI PCS EPB',
                              choices=[(-1, 'No Change'), ("00", 'OS controls EPB'), ("01", 'PECI controls EPB using PCS')],
                              default=-1)

    Energy_Performance_BIAS_Setting = RadioField('Energy Performance BIAS Setting',
                                                 choices=[(-1, 'No Change'), ("00", 'Performance'), ("07", 'Balanced Performance'), ("08", 'Balanced Power')],
                                                 default=-1)

    FRB_2_Timer = RadioField('FRB-2 Timer',
                             choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                             default=-1)

    FRB_2_Timer_timeout = RadioField('FRB-2 Timer timeout',
                                     choices=[(-1, 'No Change'), ("03", '3 Minutes '), ("04", '4 Minutes'), ("05", '5 Minutes'), ("06", '6 Minutes')],
                                     default=-1)

    Erase_SEL = RadioField('Erase SEL',
                           choices=[(-1, 'No Change'), ("00", 'No'), ("01", 'Yes, On next reset'), ("02", 'Yes, On every reset')],
                           default=-1)

    When_SEL_is_Full = RadioField('When SEL is Full',
                                  choices=[(-1, 'No Change'), ("00", 'Do Nothing'), ("01", 'Erase Immediately')],
                                  default=-1)

    Quiet_Boot = RadioField('Quiet Boot',
                            choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                            default=-1)

    Boot_mode_select = RadioField('Boot mode select',
                                  choices=[(-1, 'No Change'), ("00", 'Legacy'), ("01", 'UEFI')],
                                  default=-1)

    SATA_Controller = RadioField('SATA Controller',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    PxeDisableMask = RadioField('PxeDisableMask',
                                choices=[(-1, 'No Change'), ("00", 'Enable all port &'), ("01", 'Disable P1 &'), ("03", 'Disable P1/2...')],
                                default=-1)

    Port_0 = RadioField('Port 0',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_1 = RadioField('Port 1',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_2 = RadioField('Port 2',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_3 = RadioField('Port 3',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_4 = RadioField('Port 4',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_5 = RadioField('Port 5',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_6 = RadioField('Port 6',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    Port_7 = RadioField('Port 7',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    sSATA_Controller = RadioField('sSATA Controller',
                                  choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                  default=-1)

    Reserved = RadioField('Reserved',
                          choices=[(-1, 'No Change'), ("00", 'Select')],
                          default=-1)

    Reserved_Port_0 = RadioField('Port 0',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    Reserved_Port_1 = RadioField('Port 1',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    Reserved_Port_2 = RadioField('Port 2',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    Reserved_Port_3 = RadioField('Port 3',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    Reserved_Port_4 = RadioField('Port 4',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    Reserved_Port_5 = RadioField('Port 5',
                                 choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                 default=-1)

    OCPlan_EnDis = RadioField('OCPlan_EnDis',
                              choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                              default=-1)

    On_board_Lan = RadioField('OnboardLan',
                              choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                              default=-1)

    FastBoot = RadioField('FastBoot',
                          choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                          default=-1)

    FbSata = RadioField('FbSata',
                        choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                        default=-1)

    FbVga = RadioField('FbVga',
                       choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                       default=-1)

    FbUsb = RadioField('FbUsb',
                       choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                       default=-1)

    FbPs2 = RadioField('FbPs2',
                       choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                       default=-1)

    FbRedirection = RadioField('FbRedirection',
                               choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                               default=-1)

    FbNetworkStack = RadioField('FbNetworkStack',
                                choices=[(-1, 'No Change'), ("00", 'Disable'), ("01", 'Enable')],
                                default=-1)


class ModifyTankForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description')
    originalTank = StringField('originalTank')

    # @staticmethod
    def validate_name(self, name):
        tank = Tank.query.filter_by(tank_name=name.data).first()
        if tank is not None and (tank.tank_name != self.originalTank.data):
            raise ValidationError('Please use a different tank name')
