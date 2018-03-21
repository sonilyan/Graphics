using System;
using UnityEngine;

namespace UnityEditor.VFX
{
    [VFXInfo(category = "Math")]
    class VFXOperatorRemapToNegOnePosOne : VFXOperatorFloatUnifiedWithVariadicOutput
    {
        [VFXSetting, Tooltip("Whether the values are clamped to the input/output range")]
        public bool Clamp = false;

        public class InputProperties
        {
            [Tooltip("The value to be remapped into the new range.")]
            public FloatN input = new FloatN(0.5f);
        }

        override public string name { get { return "Remap [0..1] => [-1..1]"; } }

        protected override VFXExpression[] BuildExpression(VFXExpression[] inputExpression)
        {
            int size = VFXExpression.TypeToSize(inputExpression[0].valueType);

            VFXExpression input;

            if (Clamp)
                input = VFXOperatorUtility.Saturate(inputExpression[0]);
            else
                input = inputExpression[0];

            return new[] { VFXOperatorUtility.Mad(input, VFXOperatorUtility.TwoExpression[size], VFXOperatorUtility.Negate(VFXOperatorUtility.OneExpression[size])) };
        }
    }
}
