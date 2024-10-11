import { Field } from "formik";

type Props = {
  label?: string;
  className?: string;
  name: string;
  type?: string;
  autoComplete?: string;
  rows?: string;
  min?: string;
  onClick?: () => void;
};

function TextAreaInput({ name, label, className, rows, ...props }: Props) {
  return (
    <label className={`form-control ${className}`}>
      {label && (
        <div className="label text-gray-100">
          <span className="text-xl font-semibold prose-sm text-gray-100">
            {label}
          </span>
        </div>
      )}
      <Field
        rows={rows}
        component="textarea"
        {...props}
        name={name}
        className={`outline-none border-2 border-dashed rounded-xl p-4 border-gray-400 bg-black text-white text-xl w-full text-md`}
        placeholder={label ?? ""}
      />
    </label>
  );
}

export default TextAreaInput;
